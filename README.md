# ai-stack — plataforma pessoal de IA (100% free)

Um repositorio GitHub com um diretorio por dominio. O Git versiona e faz CI;
a execucao roda no seu host via Docker Compose;
o painel publico vive no GitHub Pages; o GPU pesado roda em notebook Kaggle.

## Estrutura

```
ai-stack/
├── portal/          dashboard estatico publicado no GitHub Pages
├── compose/         stacks docker-compose por dominio
├── services/        codigo e configuracao de cada dominio
│   ├── agent/       agente de IA (Ollama + LibreChat + OpenHands)
│   ├── image/       geracao de imagem (ComfyUI)
│   ├── video/       video (ffmpeg + moviepy + modelos locais)
│   ├── code/        scripts, snippets, helpers
│   ├── docs/        extracao/conversao de documentos
│   ├── games/       projeto Godot
│   ├── security/    varredura (Trivy, Semgrep, ZAP)
│   └── productivity/ RSS e monitoramento de paginas
├── gpu/             notebooks Kaggle (GPU gratis)
└── docs/            arquitetura e limites
```

## Como subir

1. Copie `compose/.env.example` para `compose/.env` e preencha.
2. Suba so o que precisa: `docker compose -f compose/docker-compose.agent.yml up -d`
3. O painel: `portal/` vai para o Pages no push da branch `main` (workflow `.github/workflows/pages.yml`).

## Regra de ouro

Nada aqui tem assinatura, mensalidade ou cartao. Os tetos reais estao em
`docs/ARQUITETURA.md` — leia antes de prometer algo.

## Por onde comecar

1. Leia `docs/CURSO.md` — a trilha de 10 modulos, do zero ao stack rodando.
2. Siga `COMO-SUBIR.md` para publicar este pacote no GitHub.
3. Só depois suba um dominio: `./scripts/up.sh agent`.
