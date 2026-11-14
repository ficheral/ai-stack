# Ferramentas para usar agora

Tudo aqui **abre no navegador**, sem instalar, sem cartão, sem assinatura.
Verificado em 14/11/2026.

## A nossa: PromptLab

**[Abrir o PromptLab](promptlab.html)** — chat com IA dentro do nosso próprio site,
com os prompts do ai-stack já carregados (revisor vRO, leitor de KB, documentos,
relatórios). Você usa sua chave gratuita do Google AI Studio, que fica salva só
no seu navegador.

Isso resolve o "quero usar agora": não depende de instalar Docker, nem de servidor.
Funciona no computador e no celular, do mesmo jeito.

## Para código — a prioridade do dia a dia

| Ferramenta | Link | Por que serve |
|---|---|---|
| **Google AI Studio** | https://aistudio.google.com | Gemini grátis no navegador **e** dá chave de API gratuita (é o motor do nosso PromptLab) |
| **DeepSeek** | https://chat.deepseek.com | Grátis sem plano pago, forte em apontar erro de código |
| **Qwen Chat** | https://chat.qwen.ai | Contexto de até **1 milhão de tokens** — cabe um pacote vRO inteiro |
| **Kimi** | https://kimi.com | Bom em tarefa de várias etapas |

Regra: **código sensível não vai para IA pública.** Troque IP, FQDN, senha e nome
de cliente por placeholder antes de colar.

## Imagem

| Ferramenta | Link | Nota |
|---|---|---|
| Google AI Studio (imagem) | https://aistudio.google.com | Geração e edição. O **Nano Banana** aparece aqui |
| Qwen | https://chat.qwen.ai | Geração e edição no navegador |
| Hugging Face Spaces | https://huggingface.co/spaces | Demos públicos prontos |

### O que descobri sobre Nano Banana (importante)

"Nano Banana" é o apelido do modelo de imagem do Google. **Pelo API, ele saiu do
plano gratuito** — a tabela oficial marca "Free Tier: Not available" para o
`gemini-2.5-flash-image`, a US$ 0,039 por imagem no pago (e o 2.5 tem desligamento
previsto para 15/03/2027, migrando para o 3.1 Flash Lite Image).

Ou seja: **no AI Studio (interface) você usa; por API/chave, cobra.** No PromptLab
o que funciona grátis é **texto**, não imagem.

## Documentos

| Ferramenta | Link | Nota |
|---|---|---|
| NotebookLM | https://notebooklm.google.com | Sobe PDF e ele responde **citando o trecho** |
| Stirling-PDF | `compose/docker-compose.docs.yml` | Merge, split, OCR — no seu host |

## GPU grátis

| Ferramenta | Link | Limite |
|---|---|---|
| Kaggle | https://www.kaggle.com/code | ~30 h GPU/semana, roda agendado |
| Google Colab | https://colab.research.google.com | T4, cota não publicada |

## Sobre "EventLabs"

Conferi: **não é uma IA de uso geral.** É uma startup de Rotterdam (EventLabs /
RecapHub) que vende ferramenta para **organizador de evento** — transcreve palestra,
gera clipe e resumo. É B2B, via demonstração comercial, sem plano gratuito público.

Se o seu interesse era "IA que resume reunião e gera clipe", o caminho free é
outro: NotebookLM para resumo com citação, e o `services/video/pipeline.py` para
cortar e legendar com ffmpeg no seu host.

## O que deixou de ser grátis (checado hoje)

- **Hugging Face Spaces** com Gradio/Docker: exige PRO. Free = static + 2 Spaces ZeroGPU (5 min GPU/dia).
- **Ollama Cloud**: virou pay-as-you-go.
- **Qwen Code** (CLI): cota OAuth gratuita encerrada em 15/04/2026. O Qwen Chat continua free.
- **Nano Banana por API**: sem free tier (acima).

## A regra que economiza tempo

Ferramenta grátis boa é a que você **já sabe usar**. Não troque de IA toda semana:
escolha **PromptLab** para o dia a dia do ai-stack, **DeepSeek** para código difícil
e **Qwen** para arquivo gigante. Dominar três vale mais que conhecer trinta.
