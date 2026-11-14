# Ferramentas para usar agora

Tudo aqui abre no navegador, **sem instalar, sem cartão, sem assinatura**.
Verificado em 14/11/2026.

## Para código (a prioridade que você pediu)

Seu caso: IA que **leia e explique** JavaScript do Orchestrator, PowerShell e YAML.

| Ferramenta | Link | Por que serve para você |
|---|---|---|
| **DeepSeek** | https://chat.deepseek.com | Grátis sem plano pago. O mais forte em código nos benchmarks atuais. Aceita colar arquivo ou bloco de código grande |
| **Qwen Chat** | https://chat.qwen.ai | Contexto de até **1 milhão de tokens** — cabe um pacote vRO inteiro. Melhor para "explica esse workflow completo" |
| **Google AI Studio** | https://aistudio.google.com | Gemini grátis no navegador, e ainda dá **chave de API free** para usar em script |
| **Kimi** | https://kimi.com | Bom para tarefa em várias etapas; aguenta conversa longa sem estourar limite |

### Qual usar para o quê

| Situação | Use |
|---|---|
| "Este script deu erro, o que é?" | DeepSeek — mais preciso em apontar a linha |
| "Explica este workflow de 500 linhas" | Qwen — cabe tudo de uma vez |
| "Escreva um script que faça X" | DeepSeek ou AI Studio |
| "Preciso chamar isso por API no meu código" | Google AI Studio (chave free) |

> **Aviso que vale a pena:** são serviços de terceiros. **Não cole** token, senha,
> IP interno, nome de cliente ou conteúdo de produção. Troque por placeholder
> (`vcfauto-01.exemplo.local`, `USUARIO`, `SENHA`). Para código de cliente, isso
> não é paranoia — é regra.

## Imagem

| Ferramenta | Link | Nota |
|---|---|---|
| Qwen imagem | https://chat.qwen.ai | Geração e edição no navegador, free |
| Hugging Face Spaces | https://huggingface.co/spaces | Centenas de demos públicos. Busque `flux` ou `sdxl` |
| ComfyUI local | `compose/docker-compose.image.yml` | Quando quiser controle de workflow e privacidade |

## Documentos

| Ferramenta | Link | Nota |
|---|---|---|
| Stirling-PDF | `compose/docker-compose.docs.yml` | Merge, split, OCR, assinatura — roda no seu host |
| Google Docs / LibreOffice | — | Já tem |

## Pesquisa e atualidades

| Ferramenta | Link | Nota |
|---|---|---|
| NotebookLM | https://notebooklm.google.com | Sobe PDF e ele responde **citando o trecho**. Excelente para ler KB da Broadcom |
| FreshRSS | `compose/docker-compose.productivity.yml` | Leitor de RSS no seu host |
| Google AI Studio · Deep Research | https://aistudio.google.com | Pesquisa longa com fontes |

## GPU grátis (para modelo grande)

| Ferramenta | Link | Limite |
|---|---|---|
| Kaggle | https://www.kaggle.com/code | ~30 h GPU/semana, sessão 12 h, roda agendado |
| Google Colab | https://colab.research.google.com | T4, cota não publicada |

## O que **não** é mais grátis (checado hoje)

Isto evita você perder tempo:

- **Hugging Face Spaces** com Gradio/Docker: passou a exigir PRO. Free agora = static + 2 Spaces em ZeroGPU (5 min GPU/dia).
- **Ollama Cloud**: virou pay-as-you-go.
- **Qwen Code** (o CLI): a cota OAuth gratuita acabou em 15/04/2026. O **Qwen Chat** (navegador) continua free.

## A regra que economiza seu tempo

Ferramenta free boa é a que você **já sabe usar**. Não troque de IA a cada semana:
escolha **DeepSeek para código** e **Qwen para contexto grande**, e domine as duas.
