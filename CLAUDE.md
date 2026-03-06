# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CryoVault Solutions (cryovaultsolutions.com) — a static HTML site for enterprise cyber resilience, post-quantum cold storage, and crypto security audits. Hosted on GitHub Pages with a custom domain (see `CNAME`).

## Architecture

- **Static HTML site** — no build step, no framework, no SSG. All pages are hand-written HTML with inline `<style>` blocks.
- **Design system** — CSS custom properties (design tokens) defined in `:root` on each page: `--bg-page`, `--bg-card`, `--border`, `--accent`, `--text`, `--text-bright`, `--muted`. Dark theme (slate/blue). Font: Inter via Google Fonts.
- **Shared layout pattern** — Every page has the same header (logo + nav), `<main class="main-content">`, and footer (nav + copyright). No templating — changes to nav/footer must be applied to all HTML files manually.
- **Contact form** — Tally.so embedded iframe (`442abA`). Used on `index.html` and `contact.html`.
- **SEO** — `sitemap.xml`, `sitemap.txt`, `robots.txt`, `llms.txt`. FAQ schema (JSON-LD) on homepage. When adding/removing pages, update both sitemaps.
- **Favicon** — `apple-touch-icon.png`, `favicon-32x32.png`, `favicon-16x16.png` exist at root. The `<link>` tags for these were removed from `index.html` (previously caused 404s) and need to be re-added across all pages.

## Site Structure

| Path | Purpose |
|------|---------|
| `index.html` | Homepage with service cards, FAQ schema, Tally form |
| `services/post-quantum-ready.html` | Post-quantum HSM pillar page |
| `services/cold-storage.html` | Cold storage pillar page |
| `services/cyber-resilience-audit.html` | SEC/NIS2 audit pillar page |
| `about.html` | About page |
| `contact.html` | Contact with Tally form |
| `blog/index.html` | Blog listing |
| `blog/*.html` | Blog posts |

## Key Files

- `AUDIT-GSC-AFFILIATE.md` — GSC diagnosis, affiliate strategy, content roadmap
- `PROGRESS.md` — Implementation checklist; resume work by reading this first
- `sitemap.xml` / `sitemap.txt` — Must be updated when adding or removing pages
- `llms.txt` — AI-readable site summary (referenced in robots.txt)

## Deployment

GitHub Pages from `main` branch. Push to `main` = live. No CI/CD pipeline.

## Common Tasks

- **Add a new page:** Create HTML file following the shared layout pattern (copy header/nav/footer from an existing page). Add URL to both `sitemap.xml` and `sitemap.txt`. If it's a blog post, also add an entry to `blog/index.html`.
- **Update navigation:** Must be changed in every HTML file (no shared template).
- **Resume previous work:** Read `PROGRESS.md` first, then `AUDIT-GSC-AFFILIATE.md`.
