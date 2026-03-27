#!/bin/bash
# Wrapper to run the daily news agent via Telegram Automation Orchestrator

# Move to the repository root
cd "$(dirname "$0")/.."

# If you choose to hardcode your tokens instead of exporting them globally, uncomment and fill:
# export TELEGRAM_BOT_TOKEN="your_bot_token"
# export TELEGRAM_CHAT_ID="your_chat_id"

echo "Starting Telegram Automated News Pipeline..."
python3 scripts/telegram_news_pipeline.py
