#!/usr/bin/env python3
"""Converte os .md de docs/ em paginas HTML do portal (GitHub Pages).

Roda no CI: gera _site/ com index + curso + arquitetura.
Local: python3 scripts/build_pages.py --src docs --out _site
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("falta markdown: pip install markdown", file=sys.stderr)
    raise SystemExit(1)

CSS = """
:root{--bg:#0d1117;--card:#161b22;--line:#26303d;--fg:#e6edf3;--dim:#8b949e;--acc:#4a9eff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
nav{position:sticky;top:0;background:rgba(13,17,23,.94);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);padding:14px 28px;z-index:10}
nav a{color:var(--dim);text-decoration:none;margin-right:22px;font-size:14px;font-weight:500}
nav a:hover{color:var(--acc)}
nav a.on{color:var(--fg)}
main{max-width:820px;margin:0 auto;padding:44px 28px 90px}
h1{font-size:34px;letter-spacing:-.6px;margin:0 0 6px;line-height:1.2}
h2{font-size:24px;margin:44px 0 14px;padding-top:22px;border-top:1px solid var(--line);
  letter-spacing:-.3px}
h3{font-size:18.5px;margin:30px 0 10px;color:#cdd9e5}
h4{font-size:16px;margin:22px 0 8px;color:var(--dim);text-transform:uppercase;
  letter-spacing:.5px;font-size:12.5px}
p{margin:14px 0}
a{color:var(--acc)}
code{background:#1b2230;border:1px solid var(--line);border-radius:5px;
  padding:2px 6px;font-size:13.5px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
pre{background:#0b0f16;border:1px solid var(--line);border-radius:10px;padding:16px 18px;
  overflow-x:auto;margin:18px 0}
pre code{background:none;border:none;padding:0;font-size:13px;line-height:1.55}
table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14.5px;display:block;
  overflow-x:auto}
th,td{border:1px solid var(--line);padding:9px 13px;text-align:left}
th{background:#131a24;font-weight:600}
tr:nth-child(even) td{background:#11161f}
blockquote{border-left:3px solid var(--acc);margin:18px 0;padding:2px 0 2px 18px;
  color:var(--dim);background:#10161f;border-radius:0 6px 6px 0}
ul,ol{padding-left:26px}
li{margin:7px 0}
li input[type=checkbox]{margin-right:8px}
hr{border:0;border-top:1px solid var(--line);margin:40px 0}
.meta{color:var(--dim);font-size:13.5px;margin-bottom:30px}
"""

NAV = [("/", "Painel"), ("/curso/", "Curso"), ("/arquitetura/", "Arquitetura"),
       ("/github", "Repositório")]


def page(title: str, body: str, active: str) -> str:
    links = ""
    for href, label in NAV:
        cls = ' class="on"' if href == active else ""
        target = ' target="_blank" rel="noopener"' if href == "/github" else ""
        real = "https://github.com/ficheral/ai-stack" if href == "/github" else href
        links += f'<a href="{real}"{cls}{target}>{label}</a>'
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · ai-stack</title>
<style>{CSS}</style></head>
<body>
<nav>{links}</nav>
<main>{body}</main>
</body></html>
"""


def render_md(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="docs")
    ap.add_argument("--out", default="_site")
    ap.add_argument("--portal", default="portal")
    args = ap.parse_args()

    src, out, portal = Path(args.src), Path(args.out), Path(args.portal)
    if not src.is_dir():
        print(f"sem {src}/", file=sys.stderr)
        return 1

    out.mkdir(parents=True, exist_ok=True)

    # 1. copia o portal (index.html e assets)
    for item in portal.iterdir():
        dest = out / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # 2. converte cada .md em <slug>/index.html
    paginas = []
    for md in sorted(src.glob("*.md")):
        slug = md.stem.lower().replace("_", "-")
        dest = out / slug
        dest.mkdir(exist_ok=True)
        titulo = md.stem.replace("_", " ").replace("-", " ").title()
        # primeira linha "# Titulo" define o <title>
        for line in md.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                titulo = line[2:].strip()
                break
        corpo = render_md(md)
        (dest / "index.html").write_text(
            page(titulo, corpo, f"/{slug}/"), encoding="utf-8"
        )
        paginas.append((slug, titulo, md.stat().st_size))
        print(f"pagina: /{slug}/  <- {md.name}  ({md.stat().st_size} B)")

    # 3. prompts/*.md -> /prompts/<slug>.html
    proms = src.parent / "prompts"
    if proms.is_dir():
        pd = out / "prompts"
        pd.mkdir(exist_ok=True)
        for md in sorted(proms.glob("*.md")):
            slug = md.stem.lower().replace("_", "-")
            titulo = slug.replace("-", " ").title()
            for line in md.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    titulo = line[2:].strip()
                    break
            (pd / f"{slug}.html").write_text(
                page(titulo, render_md(md), "/prompts/"), encoding="utf-8"
            )
            paginas.append((f"prompts/{slug}", titulo, md.stat().st_size))
            print(f"pagina: /prompts/{slug}.html <- {md.name}")

    # 4. .nojekyll para o Pages servir tudo
    (out / ".nojekyll").write_text("")

    print(f"ok: {len(paginas)} paginas em {out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
