# Adapta One 27 — como usar as IAs de lá com o nosso trabalho

## A resposta curta

**Não existe forma de um agente externo entrar na sua conta Adapta.** A documentação
oficial é explícita em dois lugares:

- *"O Adapta One 26 não oferece acesso direto às APIs das IAs disponíveis na plataforma."*
- *"Não existe forma de enviar tarefas para o Adapta One a partir de um sistema externo via API, webhook, MCP ou SDK, e receber respostas automaticamente sem humano."*

Fonte: https://docs.adapta.org/central-de-ajuda/plataforma/adapta-one-26/e-possivel-obter-a-api-das-ias-disponiveis

Isso não muda a sua vida. Muda **quem aperta o botão**: você cola o prompt, ele roda
com Claude 5.5 / GPT-6 / Gemini 3.8 em vez do modelo local. É o mesmo trabalho, com
motor melhor.

## O caminho que funciona hoje: Experts e Skills

O Adapta One tem dois lugares onde um prompt vira ativo reutilizável:

| Recurso | O que é | Onde |
|---|---|---|
| **Expert** | Um agente especializado que você cria em 4 passos | Menu de Experts |
| **Skill** | Instruções que ele segue sempre do mesmo jeito | Configurações → Skills |

### Criar o Expert "Revisor vRO" (2 minutos)

1. Abra o Adapta One 27.
2. Vá em **Experts** → criar novo.
3. Nome: `Revisor vRO`
4. Modelo sugerido: **Kimi K2.7 Code**, **DeepSeek V4 Pro** ou **Claude 5.5 Sonnet**
   (os três são bons em código; Kimi é o mais forte em tarefa multi-etapa).
5. Descrição: *Revisa JavaScript do Orchestrator e diz se roda no Rhino.*
6. **Instruções:** cole o bloco abaixo.
7. Salvar. Depois é só chamar `@Revisor vRO`.

### Instruções — cole isto

```
Você é revisor de código do VMware Aria Automation Orchestrator (vRO) 9.1
embarcado. Seu trabalho é apontar defeito, não elogiar.

AMBIENTE (vRO 9.1 = Rhino 1.8.0; 9.0 = 1.7.15):
- ES5 é o default portátil. Em 9.x rodam arrow, template string, includes e
  for..of; NÃO rodam class, spread, ?., ??, async/await, replaceAll.
  let/const: teste antes de assumir.
- Não existe require, process, fetch, document, cwd nem PATH.
  Log: System.log/debug/error. Java exposto: só java.util.*.
- Existem: JSON.parse/stringify, map/filter/indexOf, Object.keys,
  replace(/re/g), E4X e String.format(fmt,[args]) (exige array).
- Action: System.getModule("<mod>").<acao>(args) — ordem e aridade exatas.
  "Cannot find function" significa assinatura errada.
- Globais: Server.findForType("<tipo>", id|nome), getWorkflowWithId(id).
- REST: RESTHostManager.createTransientHostFrom(RESTHostManager.createHost("x"))
  e host.createRequest(metodo,url,corpo).execute().contentAsString.
- XML = E4X (new XML(s), .@attr, ..); não serializa direto: toXMLString().
- *_Task do vCenter é assíncrono: sem vim3WaitTaskEnd(task,true,1) o erro
  aparece depois.
- Falhar: throw "msg" ou new Error(). new WorkflowException() — confirmar.
- Action tem UM return; sem binding OUT o valor se perde em silêncio.
  Input não vinculado chega null.
- Atributo de workflow: letra inicial, sem espaço/acento/hífen. Item com
  catch-name exige throw-bind-name, senão o vRO recusa com
  "Exception binding was not set".

FORMATO:
**Veredito:** roda / quebra / roda com risco
**Problemas:** linha N → o que é → correção
**Versão corrigida:** ES5 completo, pronto para colar

Nunca invente plugin, classe ou método do vRO. Se faltar informação, pergunte.
```

Os outros três (leitor de KB, documentos, relatórios) seguem o mesmo processo —
os textos estão em https://ficheral.github.io/ai-stack/agentes/

## O caminho que vai funcionar depois: Maestro com MCP

Aqui está a parte boa que eu descobri na documentação do Maestro:

> O Maestro aceita **"Adicionar via URL"** em Conectores, e a terceira forma de
> conectar sistemas próprios é **por conector MCP personalizado**.

Ou seja: **o Maestro sabe falar MCP.** Ele consegue entrar num servidor MCP nosso.

O que falta para isso funcionar:

```
[Maestro] --MCP--> [servidor MCP do ai-stack] --Docker--> serviços
   ↑                          ↑
   seu lado                   precisa de URL pública
```

Para o Maestro alcançar o nosso MCP, ele precisa de um endereço na internet. É
exatamente o que falta: subir o ai-stack numa VM (Codespaces/Oracle) com túnel
(Cloudflare Tunnel ou Tailscale Funnel).

**Quando isso existir, aí sim os dois mundos se falam** — o Adapta chama as
ferramentas do ai-stack, em vez de você copiar e colar.

## O que NÃO fazer

- **Não dê sua senha do Adapta para nenhum agente.** Nem para mim. Sem API, o único
  jeito de "entrar" seria usar sua sessão — e isso é banível e inseguro.
- **Não cole dado de cliente** no Adapta se o plano não garante não-treinamento.
  Token, IP, FQDN e nome de cliente: troque por placeholder antes.

## Ordem prática

1. **Hoje:** crie o Expert "Revisor vRO" (2 min) e use com o código do TJSP.
2. **Esta semana:** suba o Codespace (`docs/NUVEM.md`) e tenha o ai-stack rodando.
3. **Depois:** túnel público + conector MCP no Maestro. Aí a integração é real.
