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

# --- docker existe? se nao, tenta instalar conforme a distro
if ! command -v docker >/dev/null 2>&1; then
  aviso "docker nao encontrado; detectando gerenciador de pacotes..."
  SUDO=""
  command -v sudo >/dev/null 2>&1 && SUDO="sudo"

  if command -v apt-get >/dev/null 2>&1; then
    echo "  -> Debian/Ubuntu (apt-get)"
    $SUDO apt-get update -qq >/dev/null 2>&1
    $SUDO apt-get install -y -qq docker.io docker-compose-plugin >/dev/null 2>&1 \
      || $SUDO apt-get install -y -qq docker.io docker-compose >/dev/null 2>&1 || true
  elif command -v apk >/dev/null 2>&1; then
    echo "  -> Alpine (apk)"
    $SUDO apk add --no-cache docker docker-cli-compose >/dev/null 2>&1 \
      || $SUDO apk add --no-cache docker docker-compose >/dev/null 2>&1 || true
  elif command -v dnf >/dev/null 2>&1; then
    echo "  -> Fedora/RHEL (dnf)"
    $SUDO dnf install -y docker docker-compose-plugin >/dev/null 2>&1 || true
  elif command -v yum >/dev/null 2>&1; then
    echo "  -> CentOS/RHEL (yum)"
    $SUDO yum install -y docker docker-compose >/dev/null 2>&1 || true
  else
    echo "  -> nenhum gerenciador de pacotes conhecido"
  fi

  if ! command -v docker >/dev/null 2>&1; then
    # descobrir a causa real antes de mandar recriar
    if command -v apt-get >/dev/null 2>&1 || command -v apk >/dev/null 2>&1 \
       || command -v dnf >/dev/null 2>&1 || command -v yum >/dev/null 2>&1; then
      if [ -z "$SUDO" ] && [ "$(id -u)" != "0" ]; then
        erro "existe gerenciador de pacotes, mas falta root (sudo nao existe)."
        echo "  Rode como root, ou no Codespace com sudo disponivel."
        exit 1
      fi
      erro "gerenciador existe mas a instalacao falhou (rede? repositorio?)."
      echo "  Tente na mao e veja o erro real:"
      command -v apk >/dev/null 2>&1 && echo "    apk add docker docker-cli-compose"
      command -v apt-get >/dev/null 2>&1 && echo "    apt-get install -y docker.io"
      exit 1
    fi
    erro "esta imagem nao tem gerenciador de pacotes: nao da para instalar docker."
    echo
    echo "  RECRIE o Codespace para ele usar o .devcontainer do repo:"
    echo "    1. github.com/codespaces"
    echo "    2. tres pontinhos na maquina -> Delete"
    echo "    3. New codespace -> ficheral/ai-stack -> 2-core"
    echo
    echo "  SEM docker, isto ainda funciona (nao precisa de nada):"
    echo "    python3 scripts/lint_repo.py"
    echo "    python3 scripts/build_pages.py --src docs --out site"
    echo "    python3 services/code/relatorio_vms.py --help"
    exit 1
  fi
  ok "docker instalado"
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
