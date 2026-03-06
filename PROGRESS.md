# CryoVault Solutions — Implementation Progress

**Purpose:** Resume work after a session change or crash. When you prompt **"pls continue where you left off"**, open this file and `AUDIT-GSC-AFFILIATE.md`, then do the first unchecked item under **Next** (or finish **In progress**), and update this file as you go.

---

## Completed

- [x] Fix 404s: removed broken favicon links from `index.html`
- [x] Align schema: replaced FAQ schema with enterprise/crypto audit and post-quantum FAQs in `index.html`
- [x] Add sitemap.xml and update sitemap.txt with all indexable URLs
- [x] Add site nav and internal links on homepage to new pages
- [x] Create pillar pages: `services/post-quantum-ready.html`, `services/cold-storage.html`, `services/cyber-resilience-audit.html`
- [x] Create `about.html`, `contact.html`
- [x] Create blog: `blog/index.html` and first post `blog/post-quantum-cryptography-migration-2026.html`
- [x] Add PROGRESS.md (this file)

---

## In progress

- (none)

---

## Next (do in order when continuing)

1. **Deploy and GSC:** Deploy the site, then in Google Search Console: submit the updated sitemap (Sitemaps → add sitemap URL), and use URL Inspection → Request indexing for key new URLs (e.g. `/services/post-quantum-ready.html`, `/blog/post-quantum-cryptography-migration-2026.html`).
2. **Add favicon assets (optional):** When you have favicon-32x32.png, favicon-16x16.png, apple-touch-icon.png at repo root, re-add the three `<link>` tags in `index.html` (and copy the same into other pages if they use a shared head).
3. **Second blog post:** Create `blog/best-cold-storage-practices-2026.html` (or next from AUDIT-GSC-AFFILIATE.md §5). Add URL to `sitemap.txt` and `sitemap.xml`.
4. **Affiliate programs:** Sign up for 1–2 (e.g. Backblaze, Wasabi, or Drata/Vanta). Add a “Recommended tools” or “Partners” section in footer or on relevant service/blog pages; insert affiliate links where natural.
5. **Ongoing:** Publish 1–2 blog posts per month from the Content Ideas list in the audit; add each new URL to sitemaps and request indexing in GSC.

---

## How to continue

1. Open **PROGRESS.md** (this file) and **AUDIT-GSC-AFFILIATE.md**.
2. Check **In progress** — if something is listed, finish it first.
3. Take the first unchecked item from **Next** and do it.
4. When done, move that item to **Completed** (add a new `- [x]` line with a short description) and remove it from **Next** (or mark it done in place).
5. If you add new tasks (e.g. from the audit or user request), append them to **Next** in order.
6. Save PROGRESS.md so the next session knows where you left off.

---

## File map (for reference)

| Path | Purpose |
|------|---------|
| `index.html` | Homepage; FAQ schema updated |
| `about.html` | About page |
| `contact.html` | Contact (links to Tally form) |
| `services/post-quantum-ready.html` | Pillar: Post-quantum ready |
| `services/cold-storage.html` | Pillar: Cold storage |
| `services/cyber-resilience-audit.html` | Pillar: Cyber-resilience audit |
| `blog/index.html` | Blog listing |
| `blog/post-quantum-cryptography-migration-2026.html` | First blog post |
| `sitemap.txt` | URL list (GSC) |
| `sitemap.xml` | XML sitemap (GSC) |
| `robots.txt` | Already references sitemap |
| `AUDIT-GSC-AFFILIATE.md` | Full audit and content ideas |
| `PROGRESS.md` | This progress file |
