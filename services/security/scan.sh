#!/usr/bin/env bash
# Varredura gratuita de um projeto: dependencias, segredos, codigo e container.
# Tudo roda local, nenhum servico pago.
set -euo pipefail

TARGET="${1:-.}"
OUT="${2:-./security-report}"

echo "[1/4] Trivy - vulnerabilidades de dependencia e imagem"
trivy fs --scanners vuln,secret --format json --output "$OUT/trivy.json" "$TARGET" || true

echo "[2/4] Trivy - configuracao (IaC / Dockerfile)"
trivy config --format json --output "$OUT/trivy-config.json" "$TARGET" || true

echo "[3/4] Semgrep - regras OWASP e segredos"
semgrep --config auto --json --output "$OUT/semgrep.json" "$TARGET" || true

echo "[4/4] Resumo"
python3 - "$OUT" <<'PY'
import json, sys, os
out = sys.argv[1]
def count(p, path):
    try:
        d = json.load(open(os.path.join(p, path)))
    except Exception:
        return "n/d"
    if path.startswith("trivy.json"):
        return sum(len(r.get("Vulnerabilities") or []) for r in d.get("Results", []))
    if path.startswith("trivy-config"):
        return sum(len(r.get("Misconfigurations") or []) for r in d.get("Results", []))
    if path.startswith("semgrep"):
        return len(d.get("results", []))
    return "n/d"
print(f"  Trivy vuln:    {count(out,'trivy.json')}")
print(f"  Trivy config:  {count(out,'trivy-config.json')}")
print(f"  Semgrep:       {count(out,'semgrep.json')}")
print(f"  Relatorios em: {out}/")
PY
