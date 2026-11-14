#!/usr/bin/env bash
# Prepara o ambiente na primeira vez que o Codespace abre.
# Roda automaticamente (postCreateCommand do devcontainer).
set -uo pipefail

echo "== ai-stack bootstrap =="

# 1. Docker instalado?
if ! command -v docker >/dev/null 2>&1; then
  echo "-> docker ausente; tentando instalar"
  sudo apt-get update -qq >/dev/null 2>&1 || true
  sudo apt-get install -y -qq docker.io docker-compose-plugin >/dev/null 2>&1 \
    || sudo apt-get install -y -qq docker.io docker-compose >/dev/null 2>&1 \
    || sudo apt-get install -y -qq docker.io >/dev/null 2>&1 || true
fi

# 2. Docker rodando?
if command -v docker >/dev/null 2>&1 && ! docker info >/dev/null 2>&1; then
  echo "-> iniciando docker"
  sudo service docker start >/dev/null 2>&1 || sudo dockerd >/dev/null 2>&1 &
  sleep 5
fi
if command -v docker >/dev/null 2>&1; then
  docker --version
else
  echo "AVISO: docker nao instalou. Rode: ./scripts/up.sh docs (ele tenta de novo)"
fi

# 2. compose plugin
docker compose version || sudo apt-get install -y docker-compose-plugin >/dev/null 2>&1 || true

# 3. .env a partir do exemplo
if [ ! -f compose/.env ]; then
  cp compose/.env.example compose/.env
  # DATA_DIR dentro do container (o /srv nao existe aqui)
  sed -i "s#^DATA_DIR=.*#DATA_DIR=/workspaces/ai-stack/.data#" compose/.env
  mkdir -p .data
  echo "-> compose/.env criado (DATA_DIR=.data)"
fi

# 4. aviso de modelo: 7B em CPU de 8 GB nao cabe bem
echo
echo "LEMBRETE: o Codespace tem 2 vCPU / 8 GB."
echo "  - LibreChat + Stirling + FreshRSS: rodam bem."
echo "  - Ollama com modelo 7B: lento. Use um modelo menor:"
echo "      docker exec -it ai-ollama ollama pull qwen2.5-coder:1.5b"
echo "  - ComfyUI (imagem): NAO rode aqui. Use o Kaggle para GPU."

echo
echo "Para subir um dominio:  ./scripts/up.sh docs"
echo "Abrir o agente:         ./scripts/up.sh agent"
