# Arquitetura — ai-stack (free)

## Principio

GitHub **nao executa** aplicacao com estado. Ele guarda o codigo, roda CI e
publica site estatico. Toda aplicacao viva (chat, gerador de imagem, leitor de
RSS) roda num host seu. Quem decide o que roda onde e o tamanho do servico.

```
   GitHub (free)                          Seu host / VM free
   ┌──────────────────┐                   ┌────────────────────────┐
   │ repo ai-stack    │──── Actions ─────▶│ docker compose         │
   │ CI               │   (2.000 min/mes  │  agente / imagem /     │
   │ Pages (painel)   │    ou 0 se repo   │  docs / produtividade  │
   └──────────────────┘    publico)       └────────────────────────┘
            │                                        │
            │ Pages = portal estatico                │ GPU pesado
            │                                        ▼
            │                            ┌────────────────────────┐
            └───────────────────────────▶│ Kaggle notebook (30h/s)│
                                         └────────────────────────┘
```

## Tetos reais do GitHub Free (verificado 14/11/2026)

| Item | Limite | Observacao |
|---|---|---|
| Repositorios | Ilimitados, publicos e privados | Sem teto de quantidade |
| Actions | **US$ 12/mes de compute** = 2.000 min Linux 2-core | **Gratis e ilimitado em repositorio publico** |
| Artefatos | 500 MB | Cache separado: 10 GB por repo |
| Packages | 500 MB | |
| Pages | **So repositorio publico** no Free | 1 GB de site, 100 GB/mes de banda (soft), 10 builds/h |
| Concorrencia | 20 jobs simultaneos | Job unico: 6 h maximo |
| Cartao | **Nao exigido** | Sem meio de pagamento, sem cobranca |

Fontes: https://github.com/pricing ·
https://docs.github.com/en/billing/reference/product-usage-included ·
https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

**Consequencia pratica:** o Pages funciona no Free porque este repositorio e
publico. Se um dia ele virar privado, o painel sai do ar — nesse caso o site
continua acessivel via `docs/` no proprio repo, ou move-se o painel para um
repositorio publico separado.

## GitHub x GitLab (por que GitHub)

| Item | GitHub Free | GitLab Free |
|---|---|---|
| CI | 2.000 min/mes; **ilimitado em repo publico** | 400 min/mes |
| Storage por projeto | sem teto de repo; 500 MB artefato | 10 GiB |
| Pages | 1 GB, repo publico | estatico, repo privado ok |
| Cartao | nao pede | pede para runner compartilhado |
| Conector com o assistente | **sim (nativo)** | nao (so API com token) |

O GitLab leva vantagem em um ponto: Pages a partir de repositorio privado.
Fora isso, o GitHub Free entrega mais e eu opero direto por ele.

## Onde cada dominio roda

| Dominio | Onde | Por que |
|---|---|---|
| Agente de IA (chat) | Host, CPU | Modelo 7B roda em CPU com folga |
| Imagem | Host com GPU **ou** Kaggle | ComfyUI em CPU e lento |
| Video | Host, CPU | ffmpeg e barato; modelo de video precisa GPU |
| Codigo | Repo + Actions | Nao precisa servico |
| Documentos | Host, CPU | OCR e conversao sao leves |
| Jogos | Pages (build web) | Godot exporta HTML5 |
| Seguranca | Actions (CLI) | Trivy/Semgrep sao ferramenta de linha |
| Produtividade | Host, CPU | RSS e monitor de pagina sao leves |
| Agente que executa | Host | OpenHands precisa de Docker socket |

## Host gratuito: o que existe de verdade

| Opcao | O que da | Pegadinha |
|---|---|---|
| **Oracle Always Free** | VM ARM 2 OCPU / 12 GB + 200 GB disco + 10 TB egress | Cortado de 4/24 em 15/06/2026. Capacidade escassa; instancia ociosa pode ser recuperada |
| **Kaggle** | ~30 h GPU/semana (P100 ou 2x T4) | Nao e servidor: sessao morre em 12 h |
| **Colab free** | T4 | Cota nao publicada, sem agendamento desde 03/2026 |
| **Seu proprio hardware** | Sem teto | Precisa estar ligado e acessivel |

2 OCPU / 12 GB nao roda tudo junto. Rode **um dominio por vez**, ou use o host
para agente + documentos + produtividade, e deixe imagem/video para o Kaggle.

## O que NAO colocar aqui

- Wazuh, Grafana, Elastic, n8n com muitos workflows — cada um quer um host.
- Modelo de video (LTX, Wan) em CPU: nao termina em tempo util.
- Segredo no repositorio. Use Actions Secrets ou `.env` fora do git.
- Nada de dado de cliente no `portal/`: tudo que vai para o Pages e **publico**.

## Licencas — cada escolha e por um motivo

| Peca | Licenca | Pode usar livre? |
|---|---|---|
| Ollama | MIT | Sim |
| LibreChat | MIT | Sim (escolhido no lugar do Open WebUI) |
| Open WebUI | Licenca propria | Restringe uso comercial e marca — **evitado** |
| ComfyUI | GPL-3.0 | Sim (se distribuir, distribui o codigo) |
| Stirling-PDF | MIT (core) | Sim; pastas `proprietary/` nao |
| FreshRSS | AGPL-3.0 | Sim para uso proprio |
| changedetection.io | Apache-2.0 | Sim |
| Trivy | Apache-2.0 | Sim |
| Semgrep | LGPL-2.1 | Sim |
| Godot | MIT | Sim |
| n8n | Sustainable Use License | Uso interno ok; revender nao |
