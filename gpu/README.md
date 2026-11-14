# GPU gratuita (Kaggle)

O job pesado nao roda no servidor: roda em notebook Kaggle, que da
**~30 h de GPU por semana** (P100 ou 2x T4), sessoes de ate 12 h e execucao
agendada diaria/semanal. O repositorio guarda o notebook; o codigo e versionado
aqui e o resultado volta como artefato.

| Recurso | Kaggle gratis | Colab gratis |
|---|---|---|
| GPU | 1x P100 ou 2x T4 | 1x T4 |
| Cota | ~30 h/semana (publicada) | nao publicada |
| Sessao | 12 h | ~12 h |
| Roda com aba fechada | Sim (Save & Run All) | Nao |
| Agendamento | diario/semanal/mensal | removido em 03/2026 |
| Disco salvo | 20 GB | nenhum |

Para gerar imagem e video com modelo local gratis, este e o caminho:
o modelo nao cabe em CPU de servidor pequeno, mas cabe numa T4.

## Padrao de uso

1. Notebook em `gpu/<dominio>_<tarefa>.ipynb`.
2. Publica como Kaggle Notebook, anexando o dataset do repo.
3. Schedule diario/semanal; resultado vai para o output do notebook.
4. O que der certo vira script em `services/` e roda local.
