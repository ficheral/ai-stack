#!/usr/bin/env bash
# Instala o Docker num Codespace/container Alpine, SEM rc-service nem systemctl.
# Container nao tem init: o daemon tem que ser iniciado direto com dockerd.
#
# Uso (do diretorio do repo OU de qualquer lugar):
#   bash scripts/instalar-docker.sh
set -uo pipefail

V=$'\033[0;32m'; R=$'\033[0;31m'; A=$'\033[0;33m'; N=$'\033[0m'
ok(){ echo "${V}ok${N}  $*"; }
erro(){ echo "${R}erro${N} $*" >&2; }
aviso(){ echo "${A}aviso${N} $*"; }

SUDO=""
[ "$(id -u)" != "0" ] && command -v sudo >/dev/null 2>&1 && SUDO="sudo"

echo "== 1. pacotes =="
if ! command -v docker >/dev/null 2>&1; then
  if command -v apk >/dev/null 2>&1; then
    echo "  Alpine -> apk add docker docker-cli-compose"
    $SUDO apk add --no-cache docker docker-cli-compose || { erro "apk falhou"; exit 1; }
  elif command -v apt-get >/dev/null 2>&1; then
    echo "  Debian -> apt-get install docker.io"
    $SUDO apt-get update -qq && $SUDO apt-get install -y -qq docker.io docker-compose-plugin \
      || { erro "apt falhou"; exit 1; }
  elif command -v dnf >/dev/null 2>&1; then
    $SUDO dnf install -y docker docker-compose-plugin || { erro "dnf falhou"; exit 1; }
  elif command -v yum >/dev/null 2>&1; then
    $SUDO yum install -y docker docker-compose || { erro "yum falhou"; exit 1; }
  else
    erro "sem gerenciador de pacotes nesta imagem"; exit 1
  fi
fi
ok "docker: $(docker --version 2>/dev/null | head -1)"

echo
echo "== 2. daemon =="
if docker info >/dev/null 2>&1; then
  ok "daemon ja estava rodando"
else
  # tenta o que existir; em container quase sempre so dockerd funciona
  if command -v service >/dev/null 2>&1; then
    $SUDO service docker start >/dev/null 2>&1 || true
  fi
  if command -v rc-service >/dev/null 2>&1 && ! docker info >/dev/null 2>&1; then
    $SUDO rc-service docker start >/dev/null 2>&1 || true
  fi
  if command -v systemctl >/dev/null 2>&1 && ! docker info >/dev/null 2>&1; then
    $SUDO systemctl start docker >/dev/null 2>&1 || true
  fi

  if ! docker info >/dev/null 2>&1; then
    echo "  -> subindo dockerd direto (sem init)"
    LOG=/tmp/dockerd.log
    $SUDO nohup dockerd >"$LOG" 2>&1 &
    printf "  aguardando"
    for i in $(seq 1 20); do
      sleep 2
      if docker info >/dev/null 2>&1; then echo; break; fi
      printf "."
    done
    echo
    if ! docker info >/dev/null 2>&1; then
      erro "dockerd nao subiu em 40s. Ultimas linhas do log:"
      tail -25 "$LOG" 2>/dev/null | sed 's/^/    /'
      echo
      echo "  Causas comuns em Codespace:"
      echo "    - falta de privilegio (docker-in-docker precisa --privileged)"
      echo "    - cgroup/iptables bloqueado"
      echo "  Alternativa que funciona sempre: recrie o Codespace com o .devcontainer"
      echo "    github.com/codespaces -> Delete -> New codespace"
      exit 1
    fi
  fi
  ok "daemon rodando"
fi

echo
echo "== 3. compose =="
if docker compose version >/dev/null 2>&1; then
  ok "docker compose: $(docker compose version --short 2>/dev/null)"
elif command -v docker-compose >/dev/null 2>&1; then
  aviso "so existe docker-compose v1; o up.sh pede 'docker compose' (v2)"
  if command -v apk >/dev/null 2>&1; then
    $SUDO apk add --no-cache docker-cli-compose >/dev/null 2>&1 || true
  fi
  docker compose version >/dev/null 2>&1 && ok "v2 instalado agora"
else
  if command -v apk >/dev/null 2>&1; then
    $SUDO apk add --no-cache docker-cli-compose >/dev/null 2>&1 || true
  fi
fi

echo
ok "pronto."
echo
echo "Proximo passo (no diretorio do repo):"
echo "  cd ~/ai-stack      # ou onde o repo estiver"
echo "  ./scripts/up.sh docs"
