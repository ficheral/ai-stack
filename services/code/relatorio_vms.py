#!/usr/bin/env python3
"""Relatorio de VMs por projeto -- VCF Automation 9.1.x, org VM Apps.

O que faz
---------
Autentica no VCF Automation (troca API token por bearer) e gera, em reports/AAAA-MM/:
  - vms-por-projeto.md   tabela: projeto, VMs, ligadas, desligadas
  - vms-por-projeto.csv  o mesmo, para abrir no Excel

O que precisa
-------------
- Python 3.9+ (so biblioteca padrao: nenhum pip install)
- Variaveis de ambiente:
    VCFA_HOST      ex. vcfa.tjsp.local          (sem https://)
    VCFA_TENANT    ex. TJSP-VMs                 (nome exato da org)
    VCFA_API_TOKEN o API token criado na org    (My Account > API Tokens)
- Papel de leitura na org (403 = papel, nao token)

Como se chama
-------------
    set -a; . ./compose/.env; set +a
    python3 services/code/relatorio_vms.py --mes 2026-11
    python3 services/code/relatorio_vms.py --mes 2026-11 --insecure

Endpoints usados (VM Apps org, 9.1.1 -- ver README antes de mudar)
------------------------------------------------------------------
    POST {host}/tm/oauth/tenant/{org}/token     grant_type=refresh_token
    GET  {host}/iaas/api/projects               paginado ($top/$skip)
    GET  {host}/iaas/api/machines               paginado ($top/$skip)

Aviso: nomes de campo e de endpoint mudam entre versoes e tipos de org.
Confira no API Help Center da sua instancia antes de adaptar.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PAGE = 500


def _opener(insecure: bool) -> urllib.request.OpenerDirector:
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))


def base_url(host: str) -> str:
    """Aceita 'vcfa.exemplo.com' ou a URL completa (util para laboratorio http://)."""
    if host.startswith(("http://", "https://")):
        return host.rstrip("/")
    return f"https://{host}"


def get_token(host: str, org: str, api_token: str, op) -> str:
    url = f"{base_url(host)}/tm/oauth/tenant/{urllib.parse.quote(org)}/token"
    body = urllib.parse.urlencode(
        {"grant_type": "refresh_token", "refresh_token": api_token}
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with op.open(req, timeout=60) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        detalhe = e.read()[:300].decode("utf-8", "replace")
        dica = {
            400: "grant_type errado -- use refresh_token",
            401: "API token invalido, revogado ou de outra org",
            403: "usuario sem papel na org",
            404: "org errada -- confira VCFA_TENANT no Provider Portal",
        }.get(e.code, "ver corpo abaixo")
        raise SystemExit(f"token: HTTP {e.code} ({dica}) {detalhe}")
    except urllib.error.URLError as e:
        raise SystemExit(f"token: nao alcancei {url} -- {e.reason}")
    token = data.get("access_token")
    if not token:
        raise SystemExit(f"resposta sem access_token: {list(data)}")
    return token


def get_all(host: str, path: str, token: str, op) -> list[dict]:
    """Percorre a lista paginada e devolve todos os itens de .content[]."""
    items: list[dict] = []
    skip = 0
    while True:
        query = urllib.parse.urlencode({"$top": PAGE, "$skip": skip, "$count": "true"})
        req = urllib.request.Request(
            f"{base_url(host)}{path}?{query}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        try:
            with op.open(req, timeout=120) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise SystemExit(
                    f"{path}: HTTP {e.code} -- token bom, papel insuficiente na org "
                    f"{os.environ.get('VCFA_TENANT')}"
                )
            raise SystemExit(f"{path}: HTTP {e.code} -- {e.read()[:300].decode('utf-8','replace')}")
        page = data.get("content") or []
        items.extend(page)
        total = data.get("totalElements")
        skip += len(page)
        if not page or (isinstance(total, int) and skip >= total):
            return items


def build_report(projects, machines):
    names = {p.get("id"): p.get("name", p.get("id")) for p in projects}
    per = defaultdict(lambda: {"total": 0, "on": 0, "off": 0})
    for m in machines:
        key = names.get(m.get("projectId"), m.get("projectId") or "(sem projeto)")
        row = per[key]
        row["total"] += 1
        state = str(m.get("powerState", "")).upper()
        if state.startswith("ON"):
            row["on"] += 1
        elif state.startswith("OFF"):
            row["off"] += 1
    return per


def write_outputs(per, outdir: Path, mes: str) -> tuple[Path, Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    rows = sorted(per.items(), key=lambda kv: (-kv[1]["total"], str(kv[0])))
    md = outdir / "vms-por-projeto.md"
    csvf = outdir / "vms-por-projeto.csv"
    total = sum(r["total"] for _, r in rows)

    with md.open("w", encoding="utf-8") as fh:
        fh.write(f"# VMs por projeto -- {mes}\n\n")
        fh.write(f"Gerado em {datetime.now():%Y-%m-%d %H:%M}. Total: {total} VMs "
                 f"em {len(rows)} projetos.\n\n")
        fh.write("| Projeto | VMs | Ligadas | Desligadas |\n|---|---:|---:|---:|\n")
        for name, r in rows:
            fh.write(f"| {name} | {r['total']} | {r['on']} | {r['off']} |\n")
        fh.write(f"| **Total** | **{total}** | "
                 f"**{sum(r['on'] for _, r in rows)}** | "
                 f"**{sum(r['off'] for _, r in rows)}** |\n")

    with csvf.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["projeto", "vms", "ligadas", "desligadas"])
        for name, r in rows:
            w.writerow([name, r["total"], r["on"], r["off"]])
        w.writerow(["TOTAL", total, sum(r["on"] for _, r in rows),
                    sum(r["off"] for _, r in rows)])
    return md, csvf


def main() -> int:
    ap = argparse.ArgumentParser(description="Relatorio de VMs por projeto (VCF Automation)")
    ap.add_argument("--mes", default=datetime.now().strftime("%Y-%m"), help="AAAA-MM")
    ap.add_argument("--out", default="reports", help="diretorio base de saida")
    ap.add_argument("--insecure", action="store_true", help="ignora validacao de certificado")
    args = ap.parse_args()

    host = os.environ.get("VCFA_HOST", "").replace("https://", "").strip("/")
    org = os.environ.get("VCFA_TENANT", "")
    api_token = os.environ.get("VCFA_API_TOKEN", "")
    faltando = [k for k, v in (("VCFA_HOST", host), ("VCFA_TENANT", org),
                               ("VCFA_API_TOKEN", api_token)) if not v]
    if faltando:
        print(f"faltam variaveis: {', '.join(faltando)}", file=sys.stderr)
        return 2

    op = _opener(args.insecure)
    token = get_token(host, org, api_token, op)
    print(f"token ok ({len(token)} chars) -- org {org}")

    projects = get_all(host, "/iaas/api/projects", token, op)
    machines = get_all(host, "/iaas/api/machines", token, op)
    print(f"{len(projects)} projetos, {len(machines)} VMs lidas")

    if not machines:
        print("nenhuma VM retornada: 403, org errada ou filtro de papel",
              file=sys.stderr)
        return 1

    per = build_report(projects, machines)
    md, csvf = write_outputs(per, Path(args.out) / args.mes, args.mes)
    print(f"ok: {md}\nok: {csvf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
