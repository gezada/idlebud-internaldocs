#!/usr/bin/env python3
from pathlib import Path
import html
import sys


PORTAL_CSS = r'''
:root {
  color-scheme: dark;
  --bg: #07110c;
  --panel: #0d1c14;
  --panel-2: #11261a;
  --border: rgba(172, 255, 196, 0.16);
  --text: #f4fff7;
  --muted: #a9c7b1;
  --accent: #8df0aa;
  --accent-strong: #b8ffc9;
  --shadow: 0 20px 70px rgba(0, 0, 0, 0.28);
}
* { box-sizing: border-box; }
html { min-height: 100%; background: var(--bg); }
body {
  min-height: 100vh;
  margin: 0;
  color: var(--text);
  background:
    radial-gradient(circle at 14% 10%, rgba(93, 207, 128, .13), transparent 28rem),
    radial-gradient(circle at 92% 88%, rgba(65, 133, 91, .12), transparent 30rem),
    var(--bg);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
a { color: inherit; }
.shell { width: min(1120px, calc(100% - 40px)); margin: 0 auto; }
.hero { padding: 76px 0 38px; }
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--accent);
  font-size: .78rem;
  font-weight: 750;
  letter-spacing: .16em;
  text-transform: uppercase;
}
.eyebrow::before { content: ""; width: 28px; height: 1px; background: currentColor; }
h1 { max-width: 780px; margin: 16px 0 14px; font-size: clamp(2.35rem, 6vw, 5.25rem); line-height: .98; letter-spacing: -.055em; }
.lead { max-width: 700px; margin: 0; color: var(--muted); font-size: clamp(1rem, 2.1vw, 1.22rem); line-height: 1.7; }
.grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; padding: 18px 0 78px; }
.doc-card {
  min-height: 230px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 26px;
  padding: 28px;
  border: 1px solid var(--border);
  border-radius: 25px;
  background: linear-gradient(145deg, rgba(17, 38, 26, .94), rgba(10, 24, 16, .94));
  box-shadow: var(--shadow);
  text-decoration: none;
  transition: transform .18s ease, border-color .18s ease, background .18s ease;
}
.doc-card:hover, .doc-card:focus-visible { transform: translateY(-4px); border-color: rgba(141, 240, 170, .55); background: linear-gradient(145deg, rgba(23, 50, 34, .98), rgba(11, 28, 18, .98)); }
.doc-card.primary { border-color: rgba(141, 240, 170, .34); }
.card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 18px; }
.icon { width: 50px; height: 50px; display: grid; place-items: center; border-radius: 15px; background: rgba(141, 240, 170, .1); color: var(--accent); font-size: 1.25rem; font-weight: 800; }
.status { flex: none; padding: 7px 10px; border: 1px solid var(--border); border-radius: 999px; color: var(--muted); font-size: .72rem; font-weight: 800; letter-spacing: .09em; text-transform: uppercase; }
.status.live { color: var(--accent-strong); border-color: rgba(141, 240, 170, .33); background: rgba(141, 240, 170, .08); }
.doc-card h2 { margin: 0 0 9px; font-size: clamp(1.45rem, 3vw, 2rem); letter-spacing: -.03em; }
.doc-card p { margin: 0; color: var(--muted); line-height: 1.55; }
.open { margin-top: 26px; display: inline-flex; align-items: center; gap: 9px; color: var(--accent); font-weight: 750; }
.open::after { content: "→"; transition: transform .18s ease; }
.doc-card:hover .open::after { transform: translateX(4px); }
.footer { padding: 0 0 40px; color: var(--muted); font-size: .86rem; }
.placeholder { min-height: 100vh; display: grid; place-items: center; padding: 40px 0; }
.placeholder-card { width: min(720px, 100%); padding: 40px; border: 1px solid var(--border); border-radius: 28px; background: var(--panel); box-shadow: var(--shadow); }
.back { display: inline-flex; margin-bottom: 38px; color: var(--accent); text-decoration: none; font-weight: 750; }
.placeholder h1 { font-size: clamp(2.2rem, 7vw, 4.2rem); }
.tbd { display: inline-block; margin-top: 22px; padding: 10px 13px; border-radius: 999px; background: rgba(141, 240, 170, .09); color: var(--accent-strong); font-weight: 850; letter-spacing: .12em; }
@media (max-width: 720px) {
  .shell { width: min(100% - 26px, 1120px); }
  .hero { padding-top: 52px; }
  .grid { grid-template-columns: 1fr; padding-bottom: 54px; }
  .doc-card { min-height: 205px; padding: 23px; }
  .placeholder-card { padding: 28px 23px; }
}
'''


DOCS = [
    {
        "title": "Game Design Document",
        "label": "GDD",
        "description": "The living source of truth for Idle Bud's systems, rules, progression and gameplay decisions.",
        "href": "./gdd/",
        "status": "Available · v15",
        "live": True,
        "icon": "G",
    },
    {
        "title": "Economy",
        "label": "Economy",
        "description": "Currencies, sinks, faucets, RMT rules, marketplace logic and seasonal economic controls.",
        "href": "./economy/",
        "status": "TBD",
        "live": False,
        "icon": "$",
    },
    {
        "title": "Enemies, Drops & Craft",
        "label": "Enemies, Drops & Craft",
        "description": "Enemy catalog, encounter rewards, itemization, drop tables, materials, recipes and crafting progression.",
        "href": "./enemies-drops-craft/",
        "status": "TBD",
        "live": False,
        "icon": "E",
    },
    {
        "title": "Technology Guidelines",
        "label": "Technology Guidelines",
        "description": "Architecture, authoritative-server rules, coding standards, observability, security and deployment guidance.",
        "href": "./technology-guidelines/",
        "status": "TBD",
        "live": False,
        "icon": "T",
    },
]


def page(title: str, body: str, *, description: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description)}">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{('../' if title != 'Idle Bud Internal Docs' else './')}assets/docs-portal.css">
</head>
<body>
{body}
</body>
</html>
'''


def build_home() -> str:
    cards = []
    for doc in DOCS:
        classes = "doc-card primary" if doc["live"] else "doc-card"
        status_class = "status live" if doc["live"] else "status"
        cards.append(f'''
      <a class="{classes}" href="{doc['href']}">
        <div>
          <div class="card-top">
            <span class="icon" aria-hidden="true">{html.escape(doc['icon'])}</span>
            <span class="{status_class}">{html.escape(doc['status'])}</span>
          </div>
          <div style="margin-top: 30px">
            <h2>{html.escape(doc['title'])}</h2>
            <p>{html.escape(doc['description'])}</p>
          </div>
        </div>
        <span class="open">Open document</span>
      </a>''')

    body = f'''
  <main class="shell">
    <header class="hero">
      <span class="eyebrow">Idle Lovers · Internal</span>
      <h1>Idle Bud Internal Documentation</h1>
      <p class="lead">Central access point for the living documents that define the game, its economy, content systems and technology.</p>
    </header>
    <section class="grid" aria-label="Internal documents">
{''.join(cards)}
    </section>
    <footer class="footer">Idle Bud · Internal documentation portal</footer>
  </main>'''
    return page("Idle Bud Internal Docs", body, description="Idle Bud internal documentation portal")


def build_placeholder(title: str, description: str) -> str:
    body = f'''
  <main class="placeholder">
    <section class="shell placeholder-card">
      <a class="back" href="../">← Back to Internal Docs</a>
      <span class="eyebrow">Idle Bud · Internal</span>
      <h1>{html.escape(title)}</h1>
      <p class="lead">{html.escape(description)}</p>
      <span class="tbd">TBD</span>
    </section>
  </main>'''
    return page(f"{title} · Idle Bud", body, description=description)


def add_gdd_portal_link(gdd_path: Path) -> None:
    text = gdd_path.read_text(encoding="utf-8")
    marker = "<!-- internal-docs-navigation -->"
    if marker in text:
        return
    style = '''
<style>
.internal-docs-home{position:fixed;z-index:9999;left:18px;bottom:18px;display:inline-flex;align-items:center;gap:8px;padding:10px 13px;border:1px solid rgba(141,240,170,.35);border-radius:999px;background:rgba(7,17,12,.9);backdrop-filter:blur(10px);color:#b8ffc9!important;text-decoration:none;font:700 13px/1 system-ui,-apple-system,"Segoe UI",sans-serif;box-shadow:0 12px 30px rgba(0,0,0,.25)}
.internal-docs-home:hover{transform:translateY(-1px)}
</style>
'''
    link = f'''{marker}<a class="internal-docs-home" href="../" aria-label="Back to Idle Bud Internal Docs">← Internal Docs</a>'''
    if "</head>" in text:
        text = text.replace("</head>", style + "</head>", 1)
    if "<body" in text:
        end = text.find(">", text.find("<body"))
        text = text[: end + 1] + link + text[end + 1 :]
    else:
        raise RuntimeError("GDD HTML has no <body> element.")
    gdd_path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: build_docs_portal.py <site_dir> <gdd_html>")

    site = Path(sys.argv[1])
    gdd_path = Path(sys.argv[2])
    if not gdd_path.exists():
        raise FileNotFoundError(gdd_path)

    assets = site / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "docs-portal.css").write_text(PORTAL_CSS.strip() + "\n", encoding="utf-8")
    (site / "index.html").write_text(build_home(), encoding="utf-8")

    placeholders = {
        "economy": (
            "Economy",
            "This document will define currencies, sinks, faucets, marketplace rules, RMT controls and seasonal economic balance.",
        ),
        "enemies-drops-craft": (
            "Enemies, Drops & Craft",
            "This document will define enemies, encounters, itemization, drops, materials, recipes and crafting progression.",
        ),
        "technology-guidelines": (
            "Technology Guidelines",
            "This document will define architecture, server authority, coding standards, security, observability and deployment practices.",
        ),
    }
    for slug, (title, description) in placeholders.items():
        folder = site / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(build_placeholder(title, description), encoding="utf-8")

    add_gdd_portal_link(gdd_path)

    required = [
        site / "index.html",
        site / "gdd" / "index.html",
        site / "economy" / "index.html",
        site / "enemies-drops-craft" / "index.html",
        site / "technology-guidelines" / "index.html",
        assets / "docs-portal.css",
    ]
    for item in required:
        assert item.is_file() and item.stat().st_size > 0, f"Missing portal artifact: {item}"

    home = (site / "index.html").read_text(encoding="utf-8")
    for phrase in ["Game Design Document", "Economy", "Enemies, Drops &amp; Craft", "Technology Guidelines"]:
        assert phrase in home, f"Missing portal entry: {phrase}"

    print(f"Built internal docs portal in {site}")


if __name__ == "__main__":
    main()
