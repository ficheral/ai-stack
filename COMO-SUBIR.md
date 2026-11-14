# ai-stack — como subir este pacote no GitHub

Você já tem o repositório criado: **https://github.com/ficheral/ai-stack** (privado).
O conector que uso para o GitHub caiu depois de criar o repo, então a subida
dos 35 arquivos ficou com você — são 3 comandos.

## Opção 1 — push por HTTPS com token (2 minutos)

1. Crie um token: https://github.com/settings/tokens → **Generate new token (classic)**
   → marque o escopo **repo** → copie.
2. Descompacte o zip numa pasta e rode:

```bash
cd ai-stack-free-v1.0
git init -b main
git add -A
git commit -m "ai-stack v1.0: estrutura free por dominio"
git remote add origin https://SEU_USUARIO:SEU_TOKEN@github.com/ficheral/ai-stack.git
git push -u origin main
```

3. Apague o remote com token embutido depois do push:

```bash
git remote set-url origin https://github.com/ficheral/ai-stack.git
```

## Opção 2 — GitHub Desktop ou a interface web

A interface web aceita arrastar arquivo, mas um por um. Com o zip, a opção 1 é
mais rápida.

## Depois do push — ligar o Pages

O Pages **só funciona em repositório público** no plano Free.

1. **Settings → General → Danger Zone → Change visibility → Public.**
2. **Settings → Pages → Source: GitHub Actions.**
3. O workflow `.github/workflows/pages.yml` roda no push e publica em
   `https://ficheral.github.io/ai-stack/`.

Se preferir manter o código privado: crie um repo público só para o painel e
copie `portal/index.html` + `.github/workflows/pages.yml` para ele.

## O que conferir no Actions

O workflow tem 2 jobs: `deploy` (publica o painel) e `lint` (valida os compose
e os scripts). Se o `deploy` falhar em `configure-pages`, é porque o Pages ainda
não está em "GitHub Actions" no passo anterior.

## Onde editar

| O que | Arquivo |
|---|---|
| Endereços dos serviços no painel | `portal/index.html` (array `SERVICES`) |
| Portas, senha e caminho de dados | `compose/.env.example` → copiar para `.env` |
| Quais stacks sobem | `compose/docker-compose.<dominio>.yml` |
| Limites e decisões | `docs/ARQUITETURA.md` |

## Sobre o token

Se você preferir me passar um PAT com escopo `repo`, eu subo tudo por aqui e
ligo o Pages. O token fica no workspace, não vai para o repositório — e você
pode revogar em https://github.com/settings/tokens quando terminarmos.
