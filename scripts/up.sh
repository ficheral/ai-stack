#!/usr/bin/env bash
# Sobe um dominio. Uso: ./scripts/up.sh agent|image|docs|productivity
set -euo pipefail
DOM="${1:?uso: up.sh agent|image|docs|productivity}"
cd "$(dirname "$0")/.."
[ -f compose/.env ] || { cp compose/.env.example compose/.env; echo "criado compose/.env - ajuste antes de subir"; }

case "$DOM" in
  agent|image|docs|productivity)
    docker compose -f "compose/docker-compose.${DOM}.yml" --env-file compose/.env up -d
    echo "ok: $DOM"
    docker compose -f "compose/docker-compose.${DOM}.yml" ps
    ;;
  *) echo "dominio invalido: $DOM"; exit 1 ;;
esac
