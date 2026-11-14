#!/usr/bin/env python3
"""Converte os .md de docs/ e prompts/ em paginas HTML do portal (GitHub Pages).

IMPORTANTE: todos os links sao RELATIVOS. O site e servido em /ai-stack/, entao
link absoluto ("/curso/") levaria a ficheral.github.io/curso/ e daria 404.
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
*{box-sizing:border-box}
:root{--bg:#0a0e14;--panel:#111823;--card:#141c28;--line:#22303f;--line2:#2d3d50;
  --fg:#e8eef6;--dim:#8b9bb0;--acc:#5aa9ff;--acc2:#7ee0b8;--warn:#ffc857}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;
  -webkit-font-smoothing:antialiased}
a{color:var(--acc);text-decoration:none}
a:hover{text-decoration:underline}

/* ---- topo ---- */
header.top{border-bottom:1px solid var(--line);background:rgba(10,14,20,.82);
  backdrop-filter:blur(12px);position:sticky;top:0;z-index:50}
.top-in{max-width:1080px;margin:0 auto;display:flex;align-items:center;gap:6px;
  padding:13px 24px;flex-wrap:wrap}
.brand{font-weight:700;font-size:15px;letter-spacing:-.2px;color:var(--fg);
  margin-right:14px;display:flex;align-items:center;gap:8px}
.brand span{width:8px;height:8px;border-radius:2px;background:var(--acc);
  box-shadow:0 0 10px var(--acc)}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav a{color:var(--dim);font-size:13.5px;font-weight:500;padding:6px 11px;
  border-radius:7px;transition:.14s}
nav a:hover{color:var(--fg);background:#182231;text-decoration:none}
nav a.on{color:var(--fg);background:#172435;box-shadow:inset 0 0 0 1px var(--line2)}

/* ---- layout ---- */
main{max-width:820px;margin:0 auto;padding:46px 24px 110px}
.hero{max-width:1080px;margin:0 auto;padding:58px 24px 0}
h1{font-size:clamp(28px,4vw,40px);letter-spacing:-1px;line-height:1.15;
  margin:0 0 14px;font-weight:750}
h2{font-size:24px;letter-spacing:-.4px;margin:52px 0 16px;padding-top:26px;
  border-top:1px solid var(--line);font-weight:700}
h3{font-size:18px;margin:32px 0 10px;color:#cfdcec;font-weight:650}
h4{font-size:12px;margin:24px 0 8px;color:var(--dim);text-transform:uppercase;
  letter-spacing:1px;font-weight:700}
p{margin:15px 0}
strong{color:#fff;font-weight:650}

code{background:#1a2433;border:1px solid var(--line2);border-radius:5px;
  padding:2px 6px;font-size:13.5px;
  font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace;color:#a8d4ff}
pre{background:#0d1320;border:1px solid var(--line2);border-radius:11px;
  padding:17px 19px;overflow-x:auto;margin:20px 0;
  box-shadow:0 2px 14px rgba(0,0,0,.3)}
pre code{background:none;border:none;padding:0;font-size:13px;line-height:1.6;color:#c9d9ec}

table{border-collapse:collapse;width:100%;margin:20px 0;font-size:14px;
  display:block;overflow-x:auto;border-radius:9px;border:1px solid var(--line)}
th,td{border-bottom:1px solid var(--line);padding:10px 14px;text-align:left;vertical-align:top}
th{background:#131c28;font-weight:600;font-size:12.5px;text-transform:uppercase;
  letter-spacing:.5px;color:var(--dim)}
tr:last-child td{border-bottom:none}
tr:nth-child(even) td{background:#0e151f}

blockquote{border-left:3px solid var(--acc);margin:20px 0;padding:14px 18px;
  color:#b9c8da;background:#101a26;border-radius:0 8px 8px 0}
blockquote p{margin:6px 0}
ul,ol{padding-left:24px}
li{margin:8px 0}
li input[type=checkbox]{margin-right:9px;accent-color:var(--acc2)}
hr{border:0;border-top:1px solid var(--line);margin:46px 0}
img{max-width:100%;border-radius:9px}

/* ---- cards ---- */
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));
  max-width:1080px;margin:0 auto;padding:0 24px}
.card{display:block;background:var(--card);border:1px solid var(--line);
  border-radius:13px;padding:20px;transition:.16s;position:relative;overflow:hidden}
.card:hover{border-color:var(--acc);transform:translateY(-2px);text-decoration:none;
  box-shadow:0 8px 26px rgba(0,0,0,.35)}
.card .ico{font-size:21px;display:block;margin-bottom:12px;color:var(--acc2)}
.card .tt{font-weight:650;font-size:15.5px;margin-bottom:5px;color:var(--fg)}
.card .ds{color:var(--dim);font-size:13.5px;line-height:1.55}
.card .tag{display:inline-block;margin-top:13px;font-size:10.5px;letter-spacing:.8px;
  text-transform:uppercase;color:var(--acc);background:#12243a;
  border:1px solid #1e3c5e;padding:3px 8px;border-radius:5px;font-weight:600}
.card.off{opacity:.42}
.card.off:hover{transform:none;border-color:var(--line);box-shadow:none}

.sec{max-width:1080px;margin:0 auto;padding:34px 24px 14px;font-size:11.5px;
  letter-spacing:1.2px;text-transform:uppercase;color:var(--dim);font-weight:700}
.lead{color:#a9b8ca;font-size:17px;max-width:640px;line-height:1.6}
.sub{color:var(--dim);font-size:13.5px;margin-bottom:30px}
footer{max-width:1080px;margin:0 auto;padding:40px 24px 70px;color:var(--dim);
  font-size:12.5px;border-top:1px solid var(--line)}
"""

# (href relativo, label) - relativo a partir de qualquer pagina na raiz do site
NAV = [("index.html", "Painel"), ("curso/index.html", "Curso"),
       ("ferramentas/index.html", "Ferramentas"),
       ("agentes/index.html", "Agentes"),
       ("arquitetura/index.html", "Arquitetura")]


def page(title: str, body: str, active: str, depth: int = 0) -> str:
    up = "../" * depth
    links = ""
    for href, label in NAV:
        cls = ' class="on"' if href == active else ""
        links += f'<a href="{up}{href}"{cls}>{label}</a>'
    links += ('<a href="https://github.com/ficheral/ai-stack" target="_blank" '
              'rel="noopener">GitHub</a>')
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · ai-stack</title>
<style>{CSS}</style></head>
<body>
<header class="top"><div class="top-in">
  <a class="brand" href="{up}index.html"><span></span>ai-stack</a>
  <nav>{links}</nav>
</div></header>
<main>{body}</main>
<footer>ai-stack · plataforma pessoal de IA, tudo em plano gratuito ·
<a href="https://github.com/ficheral/ai-stack">código no GitHub</a></footer>
</body></html>
"""


def render_md(path: Path) -> str:
    return markdown.markdown(
        path.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "nl2br"],
    )


def titulo_de(path: Path, padrao_pref: str = "# ") -> str:
    t = path.stem.replace("_", " ").replace("-", " ").title()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(padrao_pref):
            return line[len(padrao_pref):].strip()
    return t


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

    # 1. portal (index.html) na raiz do site
    if portal.is_dir():
        for item in portal.iterdir():
            dest = out / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

    geradas = []

    def emitir(md: Path, pasta: str, profundidade: int, pref_titulo: str):
        slug = md.stem.lower().replace("_", "-")
        d = out / pasta if pasta else out / slug
        d.mkdir(parents=True, exist_ok=True)
        tit = titulo_de(md, pref_titulo)
        alvo = (pasta + "/" if pasta else slug + "/")
        (d / "index.html").write_text(
            page(tit, render_md(md), f"{alvo}index.html", profundidade),
            encoding="utf-8",
        )
        geradas.append(f"/{alvo}")
        print(f"pagina: /{alvo}  <- {md.name}")

    # 2. docs/*.md  ->  /<slug>/
    for md in sorted(src.glob("*.md")):
        emitir(md, "", 1, "# ")

    # 3. prompts/*.md  ->  /prompts/<slug>/
    proms = src.parent / "prompts"
    if proms.is_dir():
        for md in sorted(proms.glob("*.md")):
            slug = md.stem.lower().replace("_", "-")
            d = out / "prompts" / slug
            d.mkdir(parents=True, exist_ok=True)
            tit = titulo_de(md, "# ")
            (d / "index.html").write_text(
                page(tit, render_md(md), "prompts/index.html", 2), encoding="utf-8"
            )
            geradas.append(f"/prompts/{slug}/")
            print(f"pagina: /prompts/{slug}/  <- {md.name}")

    # 4. prompts/agents/*.md  ->  /agentes/<slug>/  + indice
    ag = proms / "agents" if proms.is_dir() else None
    if ag and ag.is_dir():
        itens = ""
        for md in sorted(ag.glob("*.md")):
            slug = md.stem.lower().replace("_", "-")
            if slug == "readme":
                continue
            d = out / "agentes" / slug
            d.mkdir(parents=True, exist_ok=True)
            tit = titulo_de(md, "# Agente:")
            (d / "index.html").write_text(
                page(tit, render_md(md), "agentes/index.html", 2), encoding="utf-8"
            )
            geradas.append(f"/agentes/{slug}/")
            itens += (f'<a class="card" href="{slug}/index.html">'
                      f'<span class="ico">◉</span><div class="tt">{html.escape(tit)}</div>'
                      f'<div class="ds">Prompt pronto para o Agent Builder</div>'
                      f'<span class="tag">agente</span></a>')
            print(f"pagina: /agentes/{slug}/  <- {md.name}")
        idx = ('<div class="hero"><h1>Agentes prontos</h1>'
               '<p class="lead">Cada agente é um prompt salvo, um modelo e as '
               'ferramentas. Copie o texto e cole no Agent Builder do LibreChat.</p>'
               '</div><div class="sec">Disponíveis</div>'
               f'<div class="grid">{itens}</div><main style="padding-top:10px">'
               '<h2>Como criar</h2><ol>'
               '<li>Suba o stack: <code>./scripts/up.sh agent</code></li>'
               '<li>Abra <code>http://localhost:3080</code></li>'
               '<li>Menu lateral → <strong>Agent Builder</strong> → Create New Agent</li>'
               '<li>Cole o prompt do agente e salve</li></ol>'
               '<blockquote><p>O prompt mora no Git, a configuração mora no banco do '
               'host. Se o banco se perder, o prompt continua aqui.</p></blockquote>'
               '</main>')
        (out / "agentes").mkdir(exist_ok=True)
        (out / "agentes" / "index.html").write_text(
            page("Agentes", idx, "agentes/index.html", 1), encoding="utf-8")

    # 5. indice de prompts
    if proms.is_dir():
        itens = ""
        for md in sorted(proms.glob("*.md")):
            slug = md.stem.lower().replace("_", "-")
            tit = titulo_de(md, "# ")
            itens += (f'<a class="card" href="{slug}/index.html">'
                      f'<span class="ico">{{}}</span><div class="tt">{html.escape(tit)}</div>'
                      f'<div class="ds">Prompt de sistema para copiar e colar</div>'
                      f'<span class="tag">prompt</span></a>')
        (out / "prompts").mkdir(exist_ok=True)
        (out / "prompts" / "index.html").write_text(
            page("Prompts", '<div class="hero"><h1>Prompts</h1><p class="lead">'
                 'Prompt de sistema é o que transforma um chat genérico em especialista '
                 'no seu ambiente.</p></div><div class="sec">Disponíveis</div>'
                 f'<div class="grid">{itens}</div>', "prompts/index.html", 1),
            encoding="utf-8")

    (out / ".nojekyll").write_text("")
    print(f"\nok: {len(geradas)} paginas + portal em {out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
