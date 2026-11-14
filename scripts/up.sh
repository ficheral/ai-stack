#!/usr/bin/env bash
# Sobe um dominio do ai-stack.
#
# Uso:  ./scripts/up.sh <dominio>
#       ./scripts/up.sh docs | agent | image | productivity | remoto
#       ./scripts/up.sh lista      (mostra o que existe)
#       ./scripts/up.sh status     (o que esta rodando)
#
# Se der "Permission denied", rode: chmod +x scripts/up.sh
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

VERDE=$'\033[0;32m'; VERM=$'\033[0;31m'; AMAR=$'\033[0;33m'; NC=$'\033[0m'
ok()   { echo "${VERDE}ok${NC}  $*"; }
erro() { echo "${VERM}erro${NC} $*" >&2; }
aviso(){ echo "${AMAR}aviso${NC} $*"; }

DOMINIOS="agent image docs productivity remoto"
ARQ="compose/docker-compose.${1:-}.yml"

if [ $# -eq 0 ]; then
  echo "uso: ./scripts/up.sh <dominio>"
  echo "dominios: $DOMINIOS"
  exit 1
fi

case "$1" in
  lista)
    echo "dominios disponiveis:"
    for d in $DOMINIOS; do
      [ -f "compose/docker-compose.$d.yml" ] && echo "  - $d"
    done
    exit 0 ;;
  status)
    docker compose ls 2>/dev/null || erro "docker nao respondeu"
    exit 0 ;;
esac

# --- docker existe e esta rodando?
if ! command -v docker >/dev/null 2>&1; then
  erro "docker nao esta instalado neste ambiente."
  echo "  No Codespace: sudo service docker start"
  echo "  No seu PC: instale Docker Desktop"
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  aviso "docker nao esta rodando; tentando iniciar..."
  sudo service docker start >/dev/null 2>&1 \
    || { erro "nao consegui iniciar o docker"; echo "  tente: sudo service docker start"; exit 1; }
  sleep 3
  docker info >/dev/null 2>&1 || { erro "docker ainda nao responde"; exit 1; }
fi

# --- dominio valido?
if [ ! -f "$ARQ" ]; then
  erro "dominio '$1' nao existe (esperava $ARQ)."
  echo "  disponiveis:"; ls compose/docker-compose.*.yml 2>/dev/null | sed 's|.*/docker-compose\.||;s|\.yml||;s|^|  - |'
  exit 1
fi

# --- .env
if [ ! -f compose/.env ]; then
  cp compose/.env.example compose/.env
  aviso "criei compose/.env — revise as senhas antes de usar em producao"
  if grep -q "^DATA_DIR=/srv" compose/.env; then
    sed -i "s#^DATA_DIR=.*#DATA_DIR=$(pwd)/.data#" compose/.env
    mkdir -p .data
    aviso "DATA_DIR ajustado para $(pwd)/.data"
  fi
fi

# --- compose v2?
if ! docker compose version >/dev/null 2>&1; then
  erro "docker compose (v2) nao esta disponivel."
  echo "  instale o plugin: sudo apt install docker-compose-plugin"
  exit 1
fi

echo "subindo dominio: $1"
if docker compose -f "$ARQ" --env-file compose/.env up -d; then
  ok "dominio '$1' no ar"
  docker compose -f "$ARQ" ps
  echo
  case "$1" in
    agent)     echo "agente:      http://localhost:3080" ;;
    image)     echo "imagem:      http://localhost:8188" ;;
    docs)      echo "documentos:  http://localhost:8080" ;;
    productivity) echo "rss:      http://localhost:8081" ;;
  esac
  echo "No Codespace: aba PORTS -> clique no cadeado/globo para abrir no navegador."
else
  erro "o compose falhou. veja o log acima."
  echo "  detalhes: docker compose -f $ARQ logs --tail=50"
  exit 1
fi
