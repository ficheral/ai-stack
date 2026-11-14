#!/usr/bin/env bash
# Descobre o ambiente e diz exatamente qual comando usar.
# Funciona em qualquer distro — nao depende de apt, yum, apk ou dnf existirem.
#
# Uso:  bash scripts/diagnostico.sh

echo "=============================================="
echo " DIAGNOSTICO DO AMBIENTE"
echo "=============================================="
echo

echo "--- distro:"
if [ -f /etc/os-release ]; then
  grep -E '^(NAME|VERSION|ID|ID_LIKE|PRETTY_NAME)=' /etc/os-release | sed 's/^/    /'
else
  echo "    /etc/os-release nao existe (imagem minima?)"
fi
echo "    kernel: $(uname -r)  arch: $(uname -m)"
echo

echo "--- gerenciador de pacotes disponivel:"
ACHOU=0
for cmd in apt-get apk dnf yum microdnf zypper pacman tdnf; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "    ENCONTRADO: $cmd -> $(command -v $cmd)"
    ACHOU=1
  fi
done
[ "$ACHOU" = "0" ] && echo "    NENHUM gerenciador encontrado (imagem sem package manager)"
echo

echo "--- ja instalado:"
for cmd in git python3 pip3 docker ffmpeg jq curl node npm; do
  if command -v "$cmd" >/dev/null 2>&1; then
    v=$("$cmd" --version 2>&1 | head -1)
    echo "    $cmd: $v"
  else
    echo "    $cmd: AUSENTE"
  fi
done
echo

echo "--- docker daemon responde?"
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    echo "    SIM ($(docker info --format '{{.ServerVersion}}' 2>/dev/null))"
  else
    echo "    NAO - docker existe mas o daemon nao respondeu"
    echo "    tente: sudo service docker start   ou   sudo dockerd &"
  fi
else
  echo "    docker nem instalado"
fi
echo

echo "--- usuario e sudo:"
echo "    usuario: $(id -un) (uid $(id -u))"
command -v sudo >/dev/null 2>&1 && echo "    sudo: disponivel" || echo "    sudo: AUSENTE"
echo

echo "=============================================="
echo " O QUE FAZER"
echo "=============================================="
if command -v apt-get >/dev/null 2>&1; then
  echo "  Debian/Ubuntu detectado. Instale o Docker com:"
  echo "    sudo apt-get update"
  echo "    sudo apt-get install -y docker.io docker-compose-plugin"
  echo "    sudo service docker start"
elif command -v apk >/dev/null 2>&1; then
  echo "  Alpine detectado. Instale o Docker com:"
  echo "    sudo apk add docker docker-cli-compose"
  echo "    sudo service docker start"
  echo "  AVISO: imagem Alpine tem libc musl; algumas imagens dos servicos"
  echo "  (LibreChat, Stirling) podem nao rodar. Prefira a base bookworm."
elif command -v dnf >/dev/null 2>&1; then
  echo "  Fedora/RHEL detectado:"
  echo "    sudo dnf install -y docker docker-compose-plugin"
  echo "    sudo systemctl start docker"
elif command -v yum >/dev/null 2>&1; then
  echo "  CentOS/RHEL antigo detectado:"
  echo "    sudo yum install -y docker docker-compose"
  echo "    sudo service docker start"
else
  echo "  Sem gerenciador de pacotes nesta imagem."
  echo "  O caminho e RECRIAR o Codespace para ele usar o .devcontainer do repo:"
  echo "    1. github.com/codespaces"
  echo "    2. tres pontinhos na maquina -> Delete"
  echo "    3. New codespace -> ficheral/ai-stack -> 2-core"
  echo
  echo "  O .devcontainer.json ja pede bookworm + docker-in-docker:2."
fi
echo
echo "--- Enquanto isso, isto funciona SEM docker e SEM instalar nada:"
if command -v python3 >/dev/null 2>&1; then
  echo "    python3 services/code/relatorio_vms.py --help   (relatorio VCF, so stdlib)"
  echo "    python3 scripts/lint_repo.py                     (valida os YAML)"
  echo "    python3 scripts/build_pages.py --src docs --out site   (gera o site)"
else
  echo "    python3 tambem ausente: imagem muito minima. Recrie o Codespace."
fi
echo
