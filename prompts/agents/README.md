# Agentes prontos para criar no LibreChat

Cada arquivo aqui é um **agente**. Para criar: painel → **Agent Builder** →
*Create New Agent* → cola o prompt → escolhe o modelo → *Create*.

O que é um agente, em uma frase: **um prompt salvo + um modelo + ferramentas**.
Não é um programa novo — é uma configuração que você reusa sem redigitar.

## Ordem de criação (faça um por vez)

| # | Agente | Para quê | Prioridade |
|---|---|---|---|
| 1 | `revisor-vro` | Lê e corrige JS/PowerShell do Orchestrator | **alta** |
| 2 | `leitor-kb` | Lê KB e doc da Broadcom e resume com citação | alta |
| 3 | `documentos` | Transforma export/docx/planilha em Markdown e resumo | média |
| 4 | `relatorios` | Gera relatório de status a partir de dados | média |

## Como criar o primeiro (o que importa hoje)

1. Suba o stack do agente: `./scripts/up.sh agent`
2. Abra `http://localhost:3080`
3. Menu lateral → **Agent Builder** → *Create New Agent*
4. Nome: `Revisor vRO`
5. Modelo: o que você subiu no Ollama (`qwen2.5-coder:7b` é o padrão)
6. Instruções: copie tudo de `prompts/agents/revisor-vro.md`
7. *Create* → depois selecione o agente no seletor de modelo e converse

## Regra que evita agente inútil

Agente bom tem **uma** responsabilidade. Se você escrever "faça código, resuma,
traduza e responda e-mail", ele faz tudo mal. Um agente por tarefa.

## Onde guardar

O prompt de cada agente vem do Git (`prompts/agents/`). A configuração criada na
UI do LibreChat fica no banco do host — então, se você perder o banco, o prompt
não se perde: está versionado aqui. É por isso que o prompt mora no repositório
e não só na interface.
