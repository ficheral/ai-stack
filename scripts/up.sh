#!/usr/bin/env bash
# Sobe um dominio do ai-stack.
#
# Uso:  ./scripts/up.sh <dominio>
#       ./scripts/up.sh docs | agent | image | productivity | remoto
#       ./scripts/up.sh lista | status
#
# Funciona em Debian/Ubuntu (apt), Alpine (apk), Fedora/RHEL (dnf/yum).
# Se der "Permission denied": chmod +x scripts/up.sh
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

VERDE=$'\033[0;32m'; VERM=$'\033[0;31m'; AMAR=$'\033[0;33m'; NC=$'\033[0m'
ok()   { echo "${VERDE}ok${NC}  $*"; }
erro() { echo "${VERM}erro${NC} $*" >&2; }
aviso(){ echo "${AMAR}aviso${NC} $*"; }

DOMINIOS="agent image docs productivity remoto"

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

ARQ="compose/docker-compose.${1}.yml"

# root ou sudo?
SUDO=""
if [ "$(id -u)" != "0" ] && command -v sudo >/dev/null 2>&1; then
  SUDO="sudo"
fi

# ---------------------------------------------------------------- 1. docker instalado
if ! command -v docker >/dev/null 2>&1; then
  aviso "docker nao encontrado; detectando gerenciador de pacotes..."
  if command -v apt-get >/dev/null 2>&1; then
    echo "  -> Debian/Ubuntu (apt-get)"
    $SUDO apt-get update -qq >/dev/null 2>&1
    $SUDO apt-get install -y -qq docker.io docker-compose-plugin >/dev/null 2>&1 \
      || $SUDO apt-get install -y -qq docker.io docker-compose >/dev/null 2>&1 || true
  elif command -v apk >/dev/null 2>&1; then
    echo "  -> Alpine (apk)"
    $SUDO apk add --no-cache docker docker-cli-compose openrc >/dev/null 2>&1 \
      || $SUDO apk add --no-cache docker docker-cli-compose >/dev/null 2>&1 \
      || $SUDO apk add --no-cache docker docker-compose >/dev/null 2>&1 || true
  elif command -v dnf >/dev/null 2>&1; then
    echo "  -> Fedora/RHEL (dnf)"
    $SUDO dnf install -y docker docker-compose-plugin >/dev/null 2>&1 || true
  elif command -v yum >/dev/null 2>&1; then
    echo "  -> CentOS/RHEL (yum)"
    $SUDO yum install -y docker docker-compose >/dev/null 2>&1 || true
  else
    erro "esta imagem nao tem gerenciador de pacotes (apt/apk/dnf/yum)."
    echo "  RECRIE o Codespace para ele aplicar o .devcontainer do repo:"
    echo "    1. github.com/codespaces"
    echo "    2. tres pontinhos na maquina -> Delete"
    echo "    3. New codespace -> ficheral/ai-stack -> 2-core (8 GB)"
    echo
    echo "  SEM docker isto ainda funciona:"
    echo "    python3 scripts/lint_repo.py"
    echo "    python3 scripts/build_pages.py --src docs --out site"
    echo "    python3 services/code/relatorio_vms.py --help"
    exit 1
  fi

  if ! command -v docker >/dev/null 2>&1; then
    erro "o gerenciador existe mas a instalacao do docker falhou."
    if [ -z "$SUDO" ] && [ "$(id -u)" != "0" ]; then
      echo "  Voce nao e root e nao ha sudo. Entre como root e rode de novo."
    else
      echo "  Rode na mao para ver o erro real:"
      command -v apk     >/dev/null 2>&1 && echo "    apk add docker docker-cli-compose"
      command -v apt-get >/dev/null 2>&1 && echo "    apt-get install -y docker.io"
    fi
    exit 1
  fi
  ok "docker instalado"
fi

# ---------------------------------------------------------------- 2. daemon rodando
if ! docker info >/dev/null 2>&1; then
  aviso "daemon do docker nao responde; tentando iniciar..."

  if command -v service >/dev/null 2>&1; then
    $SUDO service docker start >/dev/null 2>&1 || true
  fi
  if ! docker info >/dev/null 2>&1 && command -v rc-service >/dev/null 2>&1; then
    echo "  -> Alpine/OpenRC: rc-service docker start"
    $SUDO rc-service docker start >/dev/null 2>&1 || true
  fi
  if ! docker info >/dev/null 2>&1 && command -v systemctl >/dev/null 2>&1; then
    $SUDO systemctl start docker >/dev/null 2>&1 || true
  fi
  if ! docker info >/dev/null 2>&1; then
    echo "  -> iniciando dockerd em background (container/Alpine/WSL)"
    $SUDO dockerd >/tmp/dockerd.log 2>&1 &
    sleep 8
  fi
  sleep 2

  if ! docker info >/dev/null 2>&1; then
    erro "o daemon nao subiu."
    echo "  log:    tail -30 /tmp/dockerd.log"
    echo "  Alpine: rc-service docker start"
    echo "  Debian: service docker start"
    echo "  Em Codespace/container, docker-in-docker precisa de --privileged."
    exit 1
  fi
  ok "docker rodando"
fi

# ---------------------------------------------------------------- 3. compose v2
if ! docker compose version >/dev/null 2>&1; then
  erro "docker compose (v2) indisponivel."
  command -v apt-get >/dev/null 2>&1 && echo "  Debian: $SUDO apt-get install -y docker-compose-plugin"
  command -v apk     >/dev/null 2>&1 && echo "  Alpine: $SUDO apk add docker-cli-compose"
  exit 1
fi

# ---------------------------------------------------------------- 4. dominio existe
if [ ! -f "$ARQ" ]; then
  erro "dominio '$1' nao existe (esperava $ARQ)."
  echo "  disponiveis:"
  ls compose/docker-compose.*.yml 2>/dev/null | sed 's|.*/docker-compose\.||;s|\.yml||;s|^|  - |'
  exit 1
fi

# ---------------------------------------------------------------- 5. .env
if [ ! -f compose/.env ]; then
  cp compose/.env.example compose/.env
  aviso "criei compose/.env — revise as senhas antes de usar de verdade"
fi
if grep -qE "^DATA_DIR=/srv" compose/.env 2>/dev/null; then
  sed -i "s#^DATA_DIR=.*#DATA_DIR=$(pwd)/.data#" compose/.env
  mkdir -p .data
  aviso "DATA_DIR ajustado para $(pwd)/.data"
fi

# ---------------------------------------------------------------- 6. subir
echo
echo "subindo dominio: $1"
if docker compose -f "$ARQ" --env-file compose/.env up -d; then
  echo
  ok "dominio '$1' no ar"
  docker compose -f "$ARQ" ps
  echo
  case "$1" in
    agent)        echo "agente:       http://localhost:3080" ;;
    image)        echo "imagem:       http://localhost:8188" ;;
    docs)         echo "documentos:   http://localhost:8080" ;;
    productivity) echo "rss:          http://localhost:8081" ;;
  esac
  echo "Codespace: aba PORTS -> icone de globo para abrir no navegador."
else
  erro "o compose falhou. Log das ultimas linhas:"
  docker compose -f "$ARQ" logs --tail=40 2>/dev/null
  exit 1
fi
