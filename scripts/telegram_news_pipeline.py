#!/usr/bin/env python3
"""
Telegram Orchestrator for OpenClaw Daily News

This script runs OpenClaw to draft an article into `scripts/draft.json`.
It then sends the draft to a Telegram channel/user via a Bot and waits for Approval/Rejection.
If Approved, it handles generating the HTML and pushing to GitHub.
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.parse
from urllib.error import URLError

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DRAFT_PATH = os.path.join(REPO_ROOT, "scripts", "draft.json")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

class TelegramBot:
    def __init__(self, token, auth_chat_id):
        self.token = token
        self.auth_chat_id = str(auth_chat_id)
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.offset = None

    def _request(self, method, data=None):
        url = f"{self.base_url}/{method}"
        req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
        payload = None if data is None else json.dumps(data).encode('utf-8')
        try:
            with urllib.request.urlopen(req, data=payload) as response:
                return json.loads(response.read().decode('utf-8'))
        except URLError as e:
            print(f"Telegram API Error: {e}")
            return None

    def send_message(self, text, keyboard=None):
        data = {
            "chat_id": self.auth_chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if keyboard:
            data["reply_markup"] = {"inline_keyboard": keyboard}
        return self._request("sendMessage", data)

    def answer_callback(self, callback_id, text=""):
        data = {"callback_query_id": callback_id, "text": text}
        self._request("answerCallbackQuery", data)

    def delete_message(self, message_id):
        self._request("deleteMessage", {"chat_id": self.auth_chat_id, "message_id": message_id})

    def wait_for_callback(self, timeout=600):
        """Long poll until we get a callback query we care about."""
        start = time.time()
        while time.time() - start < timeout:
            data = {"timeout": 30}
            if self.offset:
                data["offset"] = self.offset
                
            res = self._request("getUpdates", data)
            if res and res.get("ok"):
                for update in res["result"]:
                    self.offset = update["update_id"] + 1
                    
                    if "callback_query" in update:
                        cb = update["callback_query"]
                        # Verify the click came from our authorized user
                        if str(cb["message"]["chat"]["id"]) != self.auth_chat_id:
                            continue
                            
                        return cb
            time.sleep(2)
        return None

def run_cmd(cmd, desc="Command"):
    print(f"Running: {desc}")
    res = subprocess.run(cmd, shell=True, cwd=REPO_ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error {desc}:\n{res.stderr}")
        return False
    return True

def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        if "--test-mode" not in sys.argv:
            print("ERROR: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment.")
            sys.exit(1)
        else:
            print("[Test Mode] Would send Telegram notification here if tokens existed.")
            sys.exit(0)

    bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    if "--test-mode" in sys.argv:
        bot.send_message("⚙️ Telegram Bot is properly configured and can reach your device!")
        print("Success: Test message sent.")
        sys.exit(0)

    # 1. Trigger OpenClaw
    print("Spawning OpenClaw agent to research and draft news...")
    bot.send_message("🤖 OpenClaw is currently researching today's Anthropic news...")
    
    # We call OpenClaw CLI. We use a placeholder command since user relies on global `openclaw`
    agent_cmd = "openclaw -f scripts/openclaw_news_prompt.md"
    success = run_cmd(agent_cmd, "OpenClaw Research")
    
    if not success or not os.path.exists(DRAFT_PATH):
        bot.send_message("❌ OpenClaw failed to generate the draft.json file.")
        sys.exit(1)

    # 2. Read Draft
    with open(DRAFT_PATH, 'r') as f:
        try:
            draft = json.load(f)
        except json.JSONDecodeError:
            bot.send_message("❌ Failed to parse OpenClaw's draft as JSON.")
            sys.exit(1)

    # 3. Present Draft to User
    sections_text = ""
    for s in draft.get("sections", []):
        if isinstance(s, dict):
            sections_text += f"• <b>{s.get('heading', '')}</b>: {s.get('body', '')[:100]}...\n"
        else:
            sections_text += f"• {s}\n"

    preview = f"📰 <b>{draft.get('title', 'Unknown')}</b>\n\n"
    preview += f"<i>{draft.get('intro', '')}</i>\n\n"
    preview += f"🔗 <b>Source:</b> <a href=\"{draft.get('ref_url', '#')}\">Read Original</a>\n\n"
    preview += f"<b>Draft Preview:</b>\n{sections_text}\n"
    preview += "Do you approve this draft to be published?"
    
    msg_res = bot.send_message(
        preview, 
        keyboard=[[
            {"text": "✅ Approve & Generate", "callback_data": "approve_draft"},
            {"text": "❌ Reject & Delete", "callback_data": "reject_draft"}
        ]]
    )
    
    if not msg_res or not msg_res.get("ok"):
        print("Failed to send draft to Telegram.")
        sys.exit(1)
        
    msg_id = msg_res["result"]["message_id"]

    print("Waiting for Telegram user approval...")
    cb = bot.wait_for_callback(timeout=7200) # Wait up to 2 hours
    if not cb:
        bot.delete_message(msg_id)
        bot.send_message("⏳ Draft approval timed out after 2 hours. Process aborted.")
        sys.exit(1)

    bot.answer_callback(cb["id"])
    
    if cb["data"] == "reject_draft":
        bot.send_message("🗑️ Draft rejected and discarded.")
        bot.delete_message(msg_id)
        if os.path.exists(DRAFT_PATH):
            os.remove(DRAFT_PATH)
        sys.exit(0)

    bot.send_message("✅ Draft approved! Modifying JSON and recompiling HTML...")
    bot.delete_message(msg_id)

    # 4. Integrate the Draft
    articles_path = os.path.join(REPO_ROOT, "scripts", "articles.json")
    with open(articles_path, 'r') as f:
        articles = json.load(f)
        
    articles.insert(0, draft)
    with open(articles_path, 'w') as f:
        json.dump(articles, f, indent=4)

    if not run_cmd("python3 scripts/generate_articles.py", "Generate HTML"):
        bot.send_message("❌ Python script `generate_articles.py` failed. Check logs.")
        sys.exit(1)

    # 5. Git Checkout, Pull Main, Branch, and Commit
    import datetime
    
    run_cmd("git checkout main")
    run_cmd("git pull origin main")
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    branch_name = f"news/{date_str}-{draft.get('slug', 'update')}"
    
    run_cmd(f"git checkout -b {branch_name}")
    run_cmd("git add scripts/articles.json news/")
    title_safe = draft.get('title', 'Update').replace('"', '')
    run_cmd(f'git commit -m "Add news article: {title_safe}"')

    # 6. Final Push Approval
    msg_res = bot.send_message(
        f"🌳 Generated and committed securely to branch: <code>{branch_name}</code>\n\nReady to push to remote Github origin?",
        keyboard=[[
            {"text": "🚀 Push to Origin", "callback_data": "push_git"},
            {"text": "🛑 Keep Local Only", "callback_data": "cancel_git"}
        ]]
    )
    msg_id = msg_res["result"]["message_id"]

    print("Waiting for push approval...")
    cb = bot.wait_for_callback(timeout=3600)
    if not cb:
        bot.send_message("⏳ Push approval timed out. Code remains committed locally.")
        bot.delete_message(msg_id)
        sys.exit(0)

    bot.answer_callback(cb["id"])
    bot.delete_message(msg_id)

    if cb["data"] == "cancel_git":
        bot.send_message("📁 Understood. Code remains on your local branch without pushing.")
        sys.exit(0)

    # 7. Push!
    bot.send_message(f"📡 Pushing <code>{branch_name}</code> to Origin...")
    if run_cmd(f"git push -u origin {branch_name}", "Git Push"):
        bot.send_message("🔥 Job Complete! Article successfully pushed.")
    else:
        bot.send_message("❌ Push failed. Check your Git credentials.")

if __name__ == "__main__":
    main()
