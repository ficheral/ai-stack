# Rodar na nuvem — sem usar o seu notebook

O seu notebook é fraco, então **nada roda nele**. Todo o ai-stack roda em máquina
virtual, de graça, e você só usa o navegador.

## A escolha, em uma tabela

| Opção | O que roda | Limite free | Serve para você? |
|---|---|---|---|
| **GitHub Codespaces** | **Tudo** (Docker, LibreChat, Stirling, FreshRSS, Ollama pequeno) | **120 core-hours/mês** = 60 h em máquina de 2 núcleos, 15 GB de disco | **Sim — é o caminho** |
| Oracle Always Free | Tudo, e ligado 24 h | 2 OCPU / 12 GB ARM, 200 GB disco | Sim, mas exige criar conta e acha capacidade escassa |
| Kaggle | Só GPU, sessão de 12 h | ~30 h GPU/semana | Sim, para imagem e vídeo |
| Colab | Só GPU, sessão curta | T4, cota não publicada | Reserva |
| Seu notebook | — | — | **Não use** |

**Por que Codespaces primeiro:** você já tem conta GitHub, o repositório já está
lá, tem Docker de verdade e abre no navegador. Não precisa cartão enquanto estiver
dentro da cota.

> 120 core-hours = 60 horas numa máquina de 2 núcleos. Não é para ficar ligado o
> mês todo: é para sessões de estudo e trabalho. **Sempre pare o Codespace ao sair**
> — parado não consome compute.

## Como abrir (o que você faz)

1. Abra https://github.com/codespaces
2. *New codespace* → repositório **ficheral/ai-stack** → máquina **2-core, 8 GB**
3. Espere o build (o `.devcontainer/` já está no repo, ele se configura sozinho)
4. No terminal que abre, rode:

```bash
chmod +x scripts/*.sh       # so se der "Permission denied" (repo antigo)
./scripts/up.sh lista       # mostra os dominios disponiveis
./scripts/up.sh docs        # Stirling-PDF - leve, sobe em segundos
```

Se aparecer `Permission denied`, o arquivo perdeu o bit de execucao. O certo e
`chmod +x scripts/up.sh`. **Ja corrigi isso no repositorio** (modo `100755`) e o
CI agora falha se alguem quebrar de novo.

5. A porta 8080 ou 3080 aparece na aba **Ports** — clique em *Open in Browser*.

Pronto: o serviço está rodando **na nuvem**, o seu notebook só mostra a tela.

## O que cabe e o que não cabe

O Codespace padrão tem 2 núcleos e 8 GB.

| Domínio | Cabe? | Observação |
|---|---|---|
| Documentos (Stirling) | **Sim**, tranquilo | Melhor primeiro teste |
| Agente (LibreChat + Ollama) | Sim, com modelo pequeno | Use `qwen2.5-coder:1.5b`, não 7B |
| Produtividade (FreshRSS) | Sim | |
| Imagem (ComfyUI) | **Não** | Precisa GPU — use Kaggle |
| Vídeo com modelo | **Não** | Use Kaggle |
| Segurança (Trivy/Semgrep) | Sim | Roda em CLI, é rápido |

## Se você quiser 24 h ligado

Aí é Oracle Always Free. Diferença: o Codespace **para** quando você fecha; a VM
Oracle fica de pé. Para serviço que precisa estar sempre no ar, Oracle.
Para aprender e trabalhar em sessão, Codespaces.

## Verificação honesta

## Se o Codespace abrir sem Docker

Sintoma: `./scripts/up.sh docs` responde *"docker nao esta instalado"*.

Causa: o Codespace foi criado **antes** do `.devcontainer/` estar correto, então
montou a imagem padrão (sem Docker). Corrigi o arquivo: base `bookworm` e
`docker-in-docker:2`, que é o que o template oficial usa.

**Correção definitiva:** apague a máquina e crie outra.
`github.com/codespaces` → nos três pontinhos da máquina → *Delete* →
*New codespace* em `ficheral/ai-stack`.

### Se `apt-get` responder "not found"

Isso significa que a imagem **não é Debian/Ubuntu** — quase sempre é **Alpine**
(que usa `apk`, não `apt`). O Codespace montou a imagem padrão porque o
`.devcontainer` não foi aplicado.

**Descubra onde você está** (funciona em qualquer distro):

```bash
bash scripts/diagnostico.sh
```

Ele diz a distro, o gerenciador de pacotes, o que já está instalado e o comando
exato para o **seu** caso.

**Alpine / Codespace padrão:**

```bash
sudo apk add docker docker-cli-compose
sudo service docker start
./scripts/up.sh docs
```

**Debian/Ubuntu:**

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo service docker start
./scripts/up.sh docs
```

> Imagem Alpine tem `musl` em vez de `glibc`. Algumas imagens dos serviços
> (LibreChat, Stirling) podem não rodar nela. O caminho bom é o Codespace
> **com** o `.devcontainer` do repo, que usa `bookworm`.

O `./scripts/up.sh` agora **tenta instalar o Docker sozinho** antes de desistir.

O Codespaces eu **não consegui testar** — abrir uma sessão exige login na sua conta
GitHub, e eu não tenho acesso ao navegador logado como você. O que está verificado:
o `devcontainer.json` é JSON válido, tem `docker-in-docker` + Python + CLI, e o
`bootstrap.sh` passa no `bash -n`.

Se o build falhar, me manda o texto do erro — ele diz a linha.
