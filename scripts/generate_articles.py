#!/usr/bin/env python3
import os
import re
import json
import datetime

BASE = "https://cryovaultsolutions.com"
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATE = datetime.datetime.now().strftime("%Y-%m-%d")

INDEX_STYLES = '''        * { box-sizing: border-box; }
        :root {
            --bg: #09090b;
            --surface: #18181b;
            --text: #fafafa;
            --accent: #3b82f6;
            --accent-muted: #60a5fa;
            --muted: #a1a1aa;
            --space: 8px;
            --radius: 16px;
            --src-ransomware: #ef4444;\n            --src-breaches: #f97316;\n            --src-storage: #10b981;\n            --src-wallets: #8b5cf6;\n            --src-other: #64748b;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); padding: 20px 16px; color: var(--text); margin: 0; -webkit-text-size-adjust: 100%; line-height: 1.6; }
        .container { max-width: 900px; margin: 0 auto; padding: clamp(40px, 6vw, 60px) 0; }
        .header { text-align: center; margin-bottom: 60px; }
        h1 { color: #fff; text-transform: uppercase; font-size: clamp(2rem, 5vw, 3rem); margin: 0 0 20px; font-weight: 700; letter-spacing: -0.03em; }
        .subtitle { color: var(--muted); font-size: clamp(1rem, 2vw, 1.2rem); margin: 0 0 30px; line-height: 1.6; max-width: 600px; margin-left: auto; margin-right: auto; }
        .articles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin: 40px 0; }
        .article-card { background: var(--surface); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: var(--radius); padding: 28px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .article-card:hover { border-color: var(--accent); box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05); transform: translateY(-2px); }
        .article-card h3 { color: #fff; margin: 0 0 12px; font-size: 1.1rem; line-height: 1.5; text-transform: uppercase; }
        .article-card p { color: var(--text); margin: 0 0 16px; font-size: 0.9rem; line-height: 1.6; }
        .article-card a { color: var(--accent); text-decoration: none; font-weight: bold; display: inline-flex; align-items: center; gap: 6px; }
        .article-card a:hover { color: var(--accent-muted); text-decoration: underline; }
        .source-tag { display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; border: 1px solid currentColor; }
        .source-ransomware { color: var(--src-ransomware); border: 1px solid var(--src-ransomware); background: rgba(0,0,0,0.2); }\n        .source-breaches { color: var(--src-breaches); border: 1px solid var(--src-breaches); background: rgba(0,0,0,0.2); }\n        .source-storage { color: var(--src-storage); border: 1px solid var(--src-storage); background: rgba(0,0,0,0.2); }\n        .source-wallets { color: var(--src-wallets); border: 1px solid var(--src-wallets); background: rgba(0,0,0,0.2); }\n        .source-other { color: var(--src-other); border: 1px solid var(--src-other); background: rgba(0,0,0,0.2); }
        .card-teaser { color: var(--muted); font-size: 0.85rem; margin: 0 0 8px; line-height: 1.5; }
        .card-meta { color: #555; font-size: 0.75rem; margin: 0; }
        footer { text-align: center; margin-top: 80px; padding: 40px 20px 0; border-top: 1px solid #333; color: var(--muted); font-size: 0.85rem; }
        a { color: var(--accent); text-decoration: none; }
        @media (max-width: 640px) { body { padding: 12px; } .container { padding: 20px 0; } h1 { margin-bottom: 16px; } }
        .btn-home { display: inline-block; background: var(--accent); color: #fff; padding: 12px 24px; border-radius: var(--radius); font-weight: bold; text-decoration: none; margin-bottom: 40px; transition: 0.2s; }
        .btn-home:hover { opacity: 0.8; }
        .article-card.hidden { display: none; }
        .ticker-wrap { display: flex; align-items: center; gap: 12px; background: var(--surface); border: 1px solid rgba(255, 255, 255, 0.08); border-left: 3px solid var(--accent); padding: 8px 16px; margin-bottom: 24px; overflow: hidden; border-radius: var(--radius); }
        .ticker-label { font-size: 0.65rem; font-weight: bold; color: var(--accent); letter-spacing: 1px; white-space: nowrap; flex-shrink: 0; }
        .ticker-track { overflow: hidden; flex: 1; }
        .ticker-list { display: flex; gap: 60px; list-style: none; margin: 0; padding: 0; white-space: nowrap; animation: ticker-scroll 40s linear infinite; }
        .ticker-list li { flex-shrink: 0; font-size: 0.8rem; }
        .ticker-list a { color: var(--text); text-decoration: none; }
        .ticker-list a:hover { color: var(--accent); }
        @keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        .ticker-wrap:hover .ticker-list { animation-play-state: paused; }
        .filter-tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 24px 0 8px; justify-content: center; }
        .tab { background: var(--surface); border: 1px solid rgba(255, 255, 255, 0.08); color: var(--muted); padding: 6px 14px; border-radius: var(--radius); font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; transition: border-color 0.15s, color 0.15s; min-height: 36px; }
        .tab:hover { border-color: var(--accent); color: var(--accent); }
        .tab.active { border-color: var(--accent); color: var(--accent); background: rgba(59, 130, 246, 0.15); }
        .results-count { font-size: 0.8rem; color: var(--muted); margin: 0 0 16px; text-align: center; }
        .pagination { display: flex; align-items: center; justify-content: center; gap: 20px; margin: 40px 0 20px; }
        .page-btn { background: var(--surface); border: 1px solid rgba(255, 255, 255, 0.08); color: var(--accent); padding: 8px 16px; font-family: inherit; font-size: 0.85rem; font-weight: bold; cursor: pointer; border-radius: var(--radius); transition: border-color 0.15s; min-height: 40px; }
        .page-btn:hover:not(:disabled) { border-color: var(--accent); }
        .page-btn:disabled { color: #444; border-color: rgba(255, 255, 255, 0.02); cursor: default; }
'''

def main():
    articles_json_path = os.path.join(REPO_ROOT, "scripts", "articles.json")
    if not os.path.exists(articles_json_path):
        return

    with open(articles_json_path, "r", encoding="utf-8") as f:
        articles_data = json.load(f)

    # Convert schema format
    ARTICLES = []
    for item in articles_data:
        ARTICLES.append({
            'title': item["title"],
            'slug': item["slug"] + ".html",
            'teaser': item.get("intro", "")[:120] + "...",
            'intro': item.get("intro", ""),
            'source': item.get("source", "other"),
            'date': item.get("date", DATE),
            'sections': item.get("sections", []),
            'meta_desc': item.get("meta_desc", ""),
            'ref_url': item.get("ref_url", "#")
        })

    cards_html = ""
    if not ARTICLES:
        cards_html = '<div class="article-card" style="grid-column: 1 / -1; text-align:center;"><p>No news published yet. Check back soon!</p></div>'
    for a in ARTICLES:
        source_tag = '<span class="source-tag source-%s">%s</span>' % (a["source"], a["source"].capitalize())
        cards_html += '        <div class="article-card" data-source="%s">\n' % a["source"]
        cards_html += '            %s\n' % source_tag
        cards_html += '            <h3><a href="/news/%s">%s</a></h3>\n' % (a["slug"], a["title"])
        cards_html += '            <p class="card-teaser">%s</p>\n' % a["teaser"].replace('"', '&quot;')
        cards_html += '            <p class="card-meta">%s</p>\n' % a["date"]
        cards_html += '        </div>\n'

    news_js = '''<script>
(function() {
  var ITEMS_PER_PAGE = 12;
  var currentPage = 1;
  var currentFilter = 'all';
  var grid = document.getElementById('newsGrid');
  var tabs = document.querySelectorAll('.tab');
  var prevBtn = document.getElementById('prevBtn');
  var nextBtn = document.getElementById('nextBtn');
  var indicator = document.getElementById('pageIndicator');
  var counter = document.getElementById('resultsCount');

  function allCards() { return Array.from(grid.querySelectorAll('.article-card')); }
  function visibleCards() { return allCards().filter(c => currentFilter === 'all' || c.dataset.source === currentFilter || !c.dataset.source); }

  function render() {
    var cards = allCards();
    var visible = visibleCards();
    var total = Math.max(1, Math.ceil(visible.length / ITEMS_PER_PAGE));
    if (currentPage > total) currentPage = total;
    var start = (currentPage - 1) * ITEMS_PER_PAGE;
    var end = start + ITEMS_PER_PAGE;

    cards.forEach(c => c.classList.add('hidden'));
    visible.forEach((c, i) => { if (i >= start && i < end) c.classList.remove('hidden'); });

    if(indicator) indicator.textContent = 'Page ' + currentPage + ' of ' + total;
    if(prevBtn) prevBtn.disabled = currentPage === 1;
    if(nextBtn) nextBtn.disabled = currentPage === total;
    if(counter) counter.textContent = visible.length + ' item' + (visible.length !== 1 ? 's' : '') + (currentFilter !== 'all' ? ' · ' + currentFilter : '');
  }

  function setFilter(f) {
    currentFilter = f; currentPage = 1;
    tabs.forEach(t => {
      var active = t.dataset.filter === f;
      t.classList.toggle('active', active);
    });
    render();
  }

  tabs.forEach(t => t.addEventListener('click', () => setFilter(t.dataset.filter)));
  if(prevBtn) prevBtn.addEventListener('click', () => { if (currentPage > 1) { currentPage--; render(); } });
  if(nextBtn) nextBtn.addEventListener('click', () => { var total = Math.ceil(visibleCards().length / ITEMS_PER_PAGE); if (currentPage < total) { currentPage++; render(); } });

  document.addEventListener('keydown', e => {
    if (['INPUT','TEXTAREA','SELECT'].indexOf(document.activeElement.tagName) !== -1) return;
    var filterKeys = ['all','ransomware','breaches','storage','wallets','other'];
    var n = parseInt(e.key, 10);
    if (n >= 1 && n <= filterKeys.length) { setFilter(filterKeys[n - 1]); return; }
    if (e.key === 'ArrowLeft' && prevBtn) prevBtn.click();
    if (e.key === 'ArrowRight' && nextBtn) nextBtn.click();
  });
  render();
})();
</script>'''

    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <title>Data Security & Cold Storage News</title>
    <style>
''' + INDEX_STYLES + '''
    </style>
</head>
<body>
<div class="container">
    <a href="/" class="btn-home">&larr; Back to Home</a>
    
    <div class="ticker-wrap" aria-label="Latest headlines">
        <span class="ticker-label">LATEST</span>
        <div class="ticker-track">
            <ul class="ticker-list">
                <li><a href="/news/">Healthcare conglomerate hit by zero-day ransomware</a></li>\n                <li><a href="/news/">Massive Azure misconfiguration exposes TBs of medical data</a></li>\n                <li><a href="/news/">Synology releases major security patch</a></li>\n                <li><a href="/news/">3-2-1 backup strategies deemed essential by CISA</a></li>\n                <li><a href="/news/">Healthcare conglomerate hit by zero-day ransomware</a></li>\n                <li><a href="/news/">Massive Azure misconfiguration exposes TBs of medical data</a></li>\n                <li><a href="/news/">Synology releases major security patch</a></li>\n                <li><a href="/news/">3-2-1 backup strategies deemed essential by CISA</a></li>
            </ul>
        </div>
    </div>

    <div class="header">
        <h1>Data Security & Cold Storage News</h1>
        <p class="subtitle">Breaking news on ransomware, catastrophic breaches, and enterprise backup architecture.</p>
    </div>

    <div class="filter-tabs" id="filterTabs">
<button class="tab active" data-filter="all" role="tab">ALL</button>\n<button class="tab" data-filter="ransomware" role="tab">Ransomware</button>\n<button class="tab" data-filter="breaches" role="tab">Breaches</button>\n<button class="tab" data-filter="storage" role="tab">Storage</button>\n<button class="tab" data-filter="wallets" role="tab">Crypto Wallets</button>\n<button class="tab" data-filter="other" role="tab">Other</button>\n
    </div>
    <p class="results-count" id="resultsCount"></p>

    <div class="articles-grid" id="newsGrid">
''' + cards_html + '''
    </div>

    <nav class="pagination" id="pagination">
        <button class="page-btn" id="prevBtn">&#8592; PREV</button>
        <span id="pageIndicator" style="color:#888;">Page 1 of 1</span>
        <button class="page-btn" id="nextBtn">NEXT &#8594;</button>
    </nav>
</div>
''' + news_js + '''
</body>
</html>'''

    # Generate index.html
    news_dir = os.path.join(REPO_ROOT, "news")
    os.makedirs(news_dir, exist_ok=True)
    with open(os.path.join(news_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Generated fully styled news/index.html")

    # Generate Individual Articles
    for a in ARTICLES:
        path = os.path.join(news_dir, a["slug"])
        sections_html = ""
        for sec in a["sections"]:
            if isinstance(sec, dict):
                sections_html += '<h2>' + sec.get("heading", "") + '</h2>\n<p style="opacity:0.85;">' + sec.get("body", "") + '</p>\n'
            else:
                sections_html += '<h2>' + str(sec) + '</h2>\n'
            
        color_val = "#ef4444"
        art_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <title>''' + a["title"] + '''</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0d0d0d; color: #e0e0e0; max-width: 800px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; }
        a { color: #ef4444; text-decoration: none; }
        a:hover { text-decoration: underline; }
        hr { border: 1px solid #333; margin: 40px 0; }
        .btn-source { display: inline-block; background: #00a1e0; color: #fff; padding: 12px 24px; border-radius: 4px; font-weight: bold; text-decoration: none; margin-top: 40px; transition: 0.2s; }
        .btn-source:hover { opacity: 0.8; transform: translateY(-1px); }
    </style>
</head>
<body>
    <a href="/news/">&larr; Back to News</a>
    <h1>''' + a["title"] + '''</h1>
    <p style="color:#888;">''' + a["date"] + ''' &middot; <span style="text-transform:uppercase; color:''' + color_val + ''';">''' + a["source"] + '''</span></p>
    <p style="font-size:1.1rem; color:#ccc;">''' + a["intro"] + '''</p>
    <hr>
''' + sections_html + '''
    <a href="''' + a["ref_url"] + '''" target="_blank" class="btn-source">Read Original Post &rarr;</a>
    <div style="margin-bottom: 80px;"></div>
</body>
</html>'''
        if not os.path.exists(path) or True: # Force overwrite for testing
            with open(path, "w", encoding="utf-8") as f:
                f.write(art_html)

if __name__ == "__main__":
    main()
