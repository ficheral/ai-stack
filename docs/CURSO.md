# Curso: do zero ao ai-stack rodando

Você nao precisa saber Git antes de comecar. Cada aula tem uma tarefa pratica
de 10 a 20 minutos. A regra e: **faca, nao leia**. Quem le tudo antes de fazer
nao aprende Git, aprende a ler sobre Git.

## Como as aulas funcionam

Tres professores, tres papeis:

| Professor | Ensina | Quando chamar |
|---|---|---|
| **Trinakia75** (eu) | Git, GitHub, Docker, a estrutura ai-stack, o painel | duvida de "como faco X aqui" |
| **VCF 9.1.x** | VCF, upgrade, Avi, storage, o ambiente de datacenter | duvida de plataforma VCF |
| **VCF Orchestrator Specialist** | vRO, workflows, actions, pacotes, JavaScript/PowerShell | duvida de automacao no Orchestrator |

Voce nao precisa decidir quem chamar: pergunte para mim e eu repasso.

## Trilha

### Modulo 0 — Entender o que vamos construir (15 min, leitura)

- O que e Git e por que nao e a mesma coisa que GitHub
- O que e um repositorio, um commit, uma branch
- O que e CI e por que ele existe
- O que e Docker e por que nao instalar tudo direto na maquina

**Pratica:** abrir https://github.com/ficheral/ai-stack e olhar a aba do repo.
Ainda esta vazio — a primeira aula preenche.

### Modulo 1 — Git na pratica (30 min)

1. Instalar Git no Windows (`winget install Git.Git`) ou usar o Git Bash
2. Configurar nome e e-mail
3. `git init`, `git status`, `git add`, `git commit`
4. Ver o que mudou: `git diff` e `git log`

**Pratica:** transformar uma pasta qualquer em repositorio e fazer 3 commits.

### Modulo 2 — GitHub e o primeiro push (30 min)

1. Token de acesso pessoal (o que e, por que nao usar senha)
2. `git remote add origin` e o que ele faz
3. `git push` e o que acontece quando falha
4. Tornar o repo publico e ligar o Pages

**Pratica:** subir o ai-stack e ver o painel no ar em `ficheral.github.io/ai-stack`.

### Modulo 3 — Docker sem medo (40 min)

1. O que e imagem e o que e container (a diferenca que importa)
2. `docker run` de um servico simples
3. O que e `docker-compose.yml`: um arquivo, varios servicos
4. Volume: por que o dado nao pode morar dentro do container
5. `docker compose up -d`, `logs`, `down`

**Pratica:** subir o LibreChat com Ollama e conversar com um modelo local.

### Modulo 4 — O ai-stack na pratica (60 min)

1. Escolher onde rodar: seu PC, Oracle Free, ou o host da empresa
2. Copiar `.env.example` para `.env` e entender cada variavel
3. Subir um dominio por vez — nao tudo junto
4. Acessar pelo navegador e resolver o primeiro erro

**Pratica:** agente de IA respondendo no navegador.

### Modulo 5 — Acesso remoto sem abrir porta (30 min)

1. Por que nao expor a porta na internet
2. Tailscale: rede privada entre seus dispositivos (free: 3 usuarios, 100 dispositivos)
3. Cloudflare Tunnel: publicar com HTTPS (precisa de dominio)
4. Quando usar cada um

**Pratica:** acessar o painel do celular, fora de casa.

### Modulo 6 — CI e automacao (30 min)

1. O que o workflow `.github/workflows/pages.yml` faz, linha por linha
2. `lint` x `deploy`: por que sao jobs separados
3. Secrets: onde guardar senha sem colocar no codigo
4. Custo zero: por que repo publico tem Actions ilimitado

**Pratica:** quebrar o YAML de proposito e ver o Actions apontar o erro.

### Modulo 7 — GPU gratis (30 min)

1. Por que modelo grande nao roda em CPU de servidor pequeno
2. Kaggle: 30 h/semana, sessao de 12 h, agendamento
3. Rodar o `gpu/image_gen.ipynb` e gerar a primeira imagem
4. Quando o resultado vira script local

**Pratica:** gerar 4 imagens no Kaggle sem gastar nada.

### Modulo 8 — Seguranca e manutencao (30 min)

1. Trivy e Semgrep: o que cada um encontra
2. Rodar `services/security/scan.sh` no proprio repo
3. Ler o relatorio sem se assustar
4. Atualizar imagem Docker sem quebrar

**Pratica:** rodar a varredura e corrigir 1 achado.

### Modulo 9 — Juntando com o seu mundo VCF (45 min)

Aqui entram os outros dois professores:

- **VCF 9.1.x**: como o ambiente VCF se conecta com automacao externa (API, token)
- **Orchestrator Specialist**: transformar um script que roda no seu PC em workflow no vRO

**Pratica:** um script do ai-stack (`services/code/`) chamando a API do VCF Automation.

As duas partes da aula estao escritas logo abaixo, pelos dois professores.

Depois do 9 vem:

- **Modulo 10** — primeiro caso de uso real: relatorio de VMs por projeto (professor VCF 9.1.x)
- **Modulo 11** — primeiro workflow de verdade no vRO (professor Orchestrator Specialist)
- **Modulo 12** — pacotes e versionamento: o `.package`, a assinatura, o import e o que vai no Git

---

## Módulo 9 — parte A: do VCF Automation para fora

*Escrito pelo professor VCF 9.1.x.*

### Fluxo de autenticação (9.x)

### Embarcado × externo

### Credencial nunca no código

### Os 3 primeiros erros

### Ajuste para o seu ambiente (TJSP) — dúvida resolvida na fonte

---

## Módulo 9 — parte B: do script local ao workflow no vRO

*Escrito pelo professor VCF Orchestrator Specialist.*

### 1. O que muda de verdade

| | Script no PC | No vRO |
|---|---|---|
| Onde roda | seu shell | appliance do Orchestrator |
| Permissão | seu usuário | conta do vRO |
| Input | argv | parâmetros da **action** |
| Saída | stdout | tipo de retorno → **output binding** |
| Estado | disco, env | nada persiste entre execuções |

Não há seu `PATH`, seu cwd nem seu arquivo de config. Segredo e parâmetro de
ambiente viram **ConfigurationElement**: atributo do pacote, consumido como input.

### 2. Ciclo mínimo

1. Script isolado, entradas e saída explícitas.
2. Teste local com `node script.js` e dado falso.
3. Publique como **action**, declarando inputs e tipo de retorno.
4. No **workflow**, input do usuário + tarefa scriptable chamando a action;
   ligue campo → parâmetro.
5. Teste no vRO com VM de laboratório e leia o log.

### 3. Git

- `.action`, `.workflow`, `input_form_*`: texto (XML/JSON), diff normal.
- `.package`: zip, binário. Versione os elementos extraídos, não o gerado.
- `signatures/`: quebra o pacote se copiada errada; omita dos elementos editados.

**Nunca commitar**: ConfigurationElement de produção, credenciais, `.package` gerado.

### 4. Três erros clássicos

1. **Tipo de retorno errado**: texto onde o binding espera `number`; falha só em execução.
2. **Supor cwd**: não existe o seu diretório; use caminho absoluto ou valor do ConfigurationElement.
3. **Credencial no código**: pertence ao ConfigurationElement e chega por input.

> Depende de versão (9.1.1): formato de `input_form_` e `signatures/` não portam
> entre versões maiores.

---

## Módulo 10 — o primeiro caso de uso real (60 min)

*Escrito pelo professor VCF 9.1.x.*

### Objetivo

Um script no `services/code/` que autentica no VCF Automation do TJSP e gera um
**relatório de VMs agrupadas por projeto** (Markdown + CSV), para fechar o
inventário do mês sem planilha manual.

Escolhi este caso porque ele lê o que você já faz à mão, **não escreve nada no
ambiente** (só `GET`), e o resultado é conferível contra a UI — três coisas que
fazem um bom primeiro caso de uso.

### Pré-requisitos

- API token criado **na org TJSP-VMs** (Módulo 9A, correção acima).
- Papel de leitura na org. Um `org_owner` serve; um usuário só de catálogo não.
- `curl`, `jq` e Python 3 no host (o relatório é montado em Python; o curl/jq
  acima servem para provar a API antes de codar).
- `VCFA_HOST`, `VCFA_TENANT=TJSP-VMs`, `VCFA_API_TOKEN` em `compose/.env`
  — e `.env` no `.gitignore`. O token **não** entra no código nem no commit.
- Onde escrever: `services/code/relatorio_vms.py` — **já escrito e testado**, está em
  `relatorio_vms.py` junto com este patch. Copie e adapte, não reescreva.

### Passos

**1. Provar o token antes de escrever código.** Um comando, uma resposta:

```bash
TOKEN=$(curl -sk -X POST "https://$VCFA_HOST/tm/oauth/tenant/$VCFA_TENANT/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: application/json' \
  -d grant_type=refresh_token -d "refresh_token=$VCFA_API_TOKEN" \
  | jq -r .access_token)
[ "$TOKEN" != "null" ] && echo OK || echo FALHOU
```

Se voltar `FALHOU`, pare aqui e leia o Módulo 9A. Não siga com um token suspeito.

**2. Ler os projetos.** Documentado para org VM Apps 9.1.1:

```bash
curl -sk -G "https://$VCFA_HOST/iaas/api/projects" \
  --data-urlencode '$top=200' --data-urlencode '$count=true' \
  -H "Authorization: Bearer $TOKEN" | jq -r '.content[] | [.id, .name] | @tsv'
```

Anote `id` e `name`. A lista paginada vem em `.content[]` (com `totalElements`);
se vier vazia, 403 ou org errada. Note o `$top` entre **aspas simples**: sem elas
o shell come `$top` e a API devolve a página padrão.

**3. Ler as VMs e o `projectId` de cada uma.** Documentado para org VM Apps 9.1.1 —
`GET /iaas/api/machines`, resposta paginada em `.content[]`, cada item com
`id`, `name`, `projectId` e `powerState`:

```bash
curl -sk -G "https://$VCFA_HOST/iaas/api/machines" \
  --data-urlencode '$top=500' --data-urlencode '$count=true' \
  -H "Authorization: Bearer $TOKEN" \
  | jq -r '.content[] | [.projectId, .name, .powerState] | @tsv'
```

Alternativa (deployments, útil para ver status de provisionamento):
`GET /deployment/api/deployments?size=200&projects=<id>` → `.content[]` com
`name` e `status`. Comece por `machines`: é o que responde "VM por projeto".

**4. Agrupar e escrever.** Duas saídas em `reports/AAAA-MM/`:
`vms-por-projeto.md` (projeto, VMs, ligadas, desligadas) e `.csv` (`;`, para o
Excel em pt-BR). O script recebe o mês em `--mes` e escreve em pasta por mês, então
não sobrescreve o relatório do mês anterior.

**5. Rodar.** Não existe serviço `code` no compose (o `services/code/` é código,
não container) — o script roda no seu shell, que é o que ele precisa:

```bash
set -a; . ./compose/.env; set +a
python3 services/code/relatorio_vms.py --mes 2026-11
```

Quando ele estiver estável, é este o momento do Módulo 9B: empacotar como action
no vRO. Não antes.

**6. Commit** do script e do `README.md` com o exemplo de uso. Do `.env`, não.

### Como você sabe que funcionou

Quatro checagens, todas verificáveis:

1. O passo 1 imprime `OK` e o token tem três partes separadas por ponto.
2. O número de projetos no relatório **bate com o Organizations/Projetos da UI**.
3. A soma de VMs por projeto é igual ao total do tenant — se não for, há projeto
   invisível ao seu papel (é o 403 disfarçado de dado faltando).
4. Rode de novo em outro dia: o arquivo novo tem a data no nome e o `git diff` só
   mexe em números, não em estrutura.

Se as quatro passarem, o caso de uso está pronto — e o mesmo esqueleto
(token → GET → agrupar → arquivo) serve para relatório de hosts, de redes ou de
datastores, trocando só o passo 3.

### Armadilhas deste módulo

| Sintoma | Causa | Correção |
|---|---|---|
| 401 | API token enviado como `Bearer` | Ele só serve para gerar o bearer |
| 404 no token | Nome da org errado | `TJSP-VMs`, exatamente como no Provider Portal |
| 403 na listagem | Papel insuficiente na org | Ajuste o papel; o token está bom |
| Relatório "vazio" mas 200 | Paginação (`$top` comido pelo shell) | Aspas simples; cheque `totalElements` |
| Para de funcionar em ~90 dias | API token expirou | Gere outro e rotacione o `.env` |

---

## Módulo 11 — seu primeiro workflow de verdade (30 min)

**Prática:** uma action ES5 que normaliza nome de VM + um workflow que a chama.
Acento e espaço em nome de VM quebram hostname, pasta de datastore e tag.

### 1) Criar a action

Inventário → **Actions** → nova pasta `com.tjsp.aula` → *Add Action* → nome `normalizarNomeVM`.
Aba **Script**: colar o código. Aba **Inputs**: `nome`, tipo `string`. **Return type**: `string`.

```js
// ES5 portátil: roda do 7.x ao 9.1. No 9.1 (Rhino 1.8.0) arrow, template string,
// includes e for..of também rodam; class, spread, ?., ?? e async/await não.
// let/const: documentado, com relato de falha — confirme com o teste do item 2b.
if (!nome) throw new Error("Informe o nome da VM.");
var n = String(nome).toLowerCase()
  .replace(/[áàâãä]/g, "a").replace(/[éèêë]/g, "e")
  .replace(/[íìîï]/g, "i").replace(/[óòôõö]/g, "o")
  .replace(/[úùûü]/g, "u").replace(/ç/g, "c")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
if (n.length === 0) throw new Error("Nome inválido: " + nome);
return n.substring(0, 80).replace(/-$/, "");
```

### 2) Criar o workflow

1. **Workflows** → *New Workflow* → nome `Aula - Normalizar Nome de VM`.
2. Aba **Inputs**: `nomeVM`, tipo `string`.
3. Aba **Schema** → *New* → atributo `nomeNormalizado`, tipo `string`.
4. Arraste um **Scriptable task** para o canvas.
5. Aba **IN** do task: `nome` = `nomeVM`.
6. Aba **OUT**: `saida` = `nomeNormalizado`.
7. No script do task (ES5):

```js
saida = System.getModule("com.tjsp.aula").normalizarNomeVM(nome);
System.log("Nome normalizado: " + saida);
```

8. **Save and run** com `nomeVM` = `Servidor Ação Ç`.

### 2b) Teste de 30 segundos — o que o seu vRO aceita

Antes de confiar em qualquer guia (inclusive neste), descubra o que a **sua**
instância aceita. Crie uma action de teste chamada `testeSintaxe` e cole:

```js
var r = [];
try { var s = "x"; r.push("var: ok"); } catch (e) { r.push("var: FALHOU"); }
try { eval("let a = 1;"); r.push("let: ok"); } catch (e) { r.push("let: FALHOU"); }
try { eval("const b = 1;"); r.push("const: ok"); } catch (e) { r.push("const: FALHOU"); }
try { eval("var f = (x) => x;"); r.push("arrow: ok"); } catch (e) { r.push("arrow: FALHOU"); }
try { eval("var t = `a${1}`;"); r.push("template: ok"); } catch (e) { r.push("template: FALHOU"); }
try { eval("var c = class {};"); r.push("class: ok"); } catch (e) { r.push("class: FALHOU"); }
try { [1].includes(1); r.push("includes: ok"); } catch (e) { r.push("includes: FALHOU"); }
return r.join(" | ");
```

O retorno diz o que roda. **Isto resolve a dúvida que ninguém consegue responder
de fora**: a documentação diz que `let`/`const` funcionam no 9.1, mas há relato de
falha no 9.0. Só a sua instância responde.

Guarde o resultado: ele vale para todo código que você escrever daqui pra frente.

### 3) O que você deve ver

- Log: `Nome normalizado: servidor-acao-c` — e o output `nomeNormalizado` igual.
- Com `nomeVM` vazio: o workflow falha com *Informe o nome da VM.* (a exceção da action sobe para o workflow — é o que você quer).
- Com `!!!`: falha com *Nome inválido*.

**O que acabou de acontecer:** a action é a função, o workflow é quem a orquestra.
O binding IN é o argumento, o OUT é o `return`. Sem OUT ligado, a action roda e o valor se perde — erro silencioso mais comum.

*Versão:* `System.getModule` existe de 7.x a 9.1. O Rhino continua o motor padrão de actions — **1.8.0 no 9.1**, 1.7.15 no 9.0. ES5 é o default portátil, não o único dialeto suportado: veja o teste do item 2b. `throw` em action aparece como erro do workflow; usar `WorkflowException` também é válido.

---

---

## Módulo 12 — pacotes e versionamento (45 min)

*Escrito por Trinakia75, a partir da proposta do professor VCF Orchestrator Specialist — formato do pacote, assinatura e caminhos de log verificados na fonte.*

Depois do Módulo 11, que é a ordem certa: você só empacota o que já existe.

### O problema que este módulo resolve

No Módulo 11 a action e o workflow viveram **só dentro do seu vRO**. Isso não é entrega: não
volta depois de um restore, não vai para o cliente, não roda em homologação. O único jeito de
tirar objeto do Orchestrator de um lado e colocar do outro é o **`.package`** — e é aí que quase
todo mundo trava, porque o pacote tem três camadas que erram em silêncio: **assinatura**,
**encoding** e **versão**.

A regra do módulo: **o pacote que importa é o que o próprio vRO gerou.** Pacote montado à mão
(ou "consertado" editando o zip) não importa. O resto do módulo é como viver com isso.

---

### 1) O que tem dentro de um `.package` (verificado em export real do 9.1.1)

Isto não é dedução: foi conferido desmontando um export real (`SnapshotxDays`, vRO 9.1.1.0100)
e reconstruindo byte a byte — 54 de 54 entradas bateram.

| Entrada | O que é | Encoding / compressão |
|---|---|---|
| `raiz/` | pasta com o nome do pacote, com entradas de **diretório explícitas** | store |
| `raiz/dunes-meta-inf` | cartão de identidade: `pkg-name`, `vso-version`, `vso-build-nb`, `used-plugins`, `pkg-id`, **`pkg-signer`**, **`pkg-owner`** | UTF-8 sem BOM |
| `raiz/certificates/<DN>.cer` | certificado do publicador (DER), com o DN no nome | store |
| `raiz/elements/<id>/` | cada objeto: `info`, `categories`, `data`, `input_form_` | `elements/` em deflate |
| `raiz/signatures/` | espelho de **todos** os arquivos, um `.sig` de 256 bytes cada | store |

- **`data`**, **`categories`** e **`input_form_`** vão em **UTF-16BE com BOM** (`FE FF`).
  `dunes-meta-inf` e `info` vão em UTF-8 **sem** BOM. Trocar isso é a causa de acento virar
  caractere estranho — ou do export de package com Unicode vir em hex.
- **A assinatura é RSA-2048, PKCS#1 v1.5 + SHA-256, sobre os bytes crus do arquivo** —
  não sobre o hash, não sobre o zip inteiro. 256 bytes por arquivo. Foi assim que as 18
  assinaturas do export de referência validaram.
- **`used-plugins`** é o campo que decide se o pacote serve no destino: lista os plugins que os
  itens usam. Plugin ausente no destino não impede o import, mas deixa o elemento órfão.

**Consequência prática, e é a mais importante do módulo:** mexer em **um byte** de um `data`
invalida a assinatura daquele arquivo. Não existe "abrir o pacote, corrigir uma linha e fechar".
Se o pacote está errado, corrija no vRO e exporte de novo.

---

### 2) O ciclo que funciona

```
elemento no vRO  →  New Package → adicionar elementos → Save
                 →  Export (gera .package assinado)
                 →  Import no destino → confiar no certificado do publicador
```

Três detalhes que mudam o resultado:

1. **`Save` sem rebuild.** Num pacote que só agrupa objetos que já existem no servidor, salve
   com **"Skip rebuilding"**. Rebuild gera IDs/estrutura próprios e é o caminho que já produziu
   `Invalid Package element type` (KB 405937).
2. **Importar não sobrescreve por acaso.** O import compara **versão por elemento**: elemento do
   pacote mais novo que o do servidor entra; mais antigo precisa ser **selecionado à mão**.
   Por API isso aparece como **409**, não como 400 — não é defeito do pacote.
3. **"Import Configuration Attribute Values"** vem **marcado** por padrão. Num pacote com
   ConfigurationElement isso significa **sobrescrever a senha de produção do cliente** pelos
   valores da sua origem. Desmarque, sempre, e diga isso no README da entrega.

---

### 3) Pré-voo de 5 minutos: culpar o pacote só depois disto

Antes de abrir log, pergunte ao próprio vRO o que ele achou do arquivo. Existe endpoint para
isso — ele analisa e devolve três booleanos separados, que é exatamente o que você precisa para
não diagnosticar no escuro:

```bash
# token do tenant (Módulo 9A) — vRO embarcado no VCF Automation 9.1
TOKEN=$(curl -sk -X POST "https://$VCFA_HOST/tm/oauth/tenant/$VCFA_TENANT/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d grant_type=refresh_token -d "refresh_token=$VCFA_API_TOKEN" | jq -r .access_token)

# análise do arquivo, SEM importar nada
curl -sk -X POST "https://$VCFA_HOST/vco/api/packages/import-details" \
  -H "Authorization: Bearer $TOKEN" -F "file=@com.tjsp.dns-13.package" \
  | jq '{packageName, packageAlreadyExists, contentVerified,
         certificateTrusted, certificateValid, certificateUnknown}'
```

| Campo | `false` significa | O que fazer |
|---|---|---|
| `contentVerified` | a assinatura **não** confere com o conteúdo | pacote corrompido ou editado à mão — exporte de novo |
| `certificateTrusted` | certificado do publicador desconhecido | é o esperado na primeira vez: aceite "trust" no import |
| `certificateValid` | certificado vencido ou fora de validade | exporte do vRO com certificado válido |
| `packageAlreadyExists` | já existe pacote com esse nome | decidir se é upgrade ou duplicata antes de importar |

O import de verdade é o mesmo endpoint sem `/import-details`, com os parâmetros explícitos —
nada de confiar no default:

```bash
curl -sk -X POST "https://$VCFA_HOST/vco/api/packages?overwrite=true\
&importConfigurationAttributeValues=false\
&importConfigSecureStringAttributeValues=false\
&tagImportMode=ImportButPreserveExistingValue" \
  -H "Authorization: Bearer $TOKEN" -F "file=@com.tjsp.dns-13.package"
```

`overwrite=true` faz o pacote vencer a comparação de versão; os dois `importConfiguration*`
em `false` são o que impede o pacote de mexer em credencial do ambiente de destino.

---

### 4) Quando falha: onde está o motivo de verdade

O erro na tela nunca diz nada útil. A mensagem real está no log do `vco-app`.

| Sintoma | Onde olhar | O que procurar |
|---|---|---|
| 400 / "Failed to import package" | `vco-server-app.log` do pod `vco-app` | linha do elemento que quebrou, ex.: `Invalid Package element type: '...Repository'` |
| 409 | resposta da API | elemento do servidor é mais novo que o do pacote |
| Import "some" e nunca volta | tamanho do pacote / gateway | KB 388745: import acima de ~5 min estoura `stream-idle-timeout` — exporte em pacotes menores |
| Import ok, item não funciona | `used-plugins` do pacote × plugins do destino | plugin ausente = objeto órfão, sem erro no import |

**Onde ficam os logs no 9.1 embarcado** (importante: o caminho do appliance externo **não**
existe aqui):

```bash
# console do Orchestrator (o equivalente ao catalina.out de antigamente)
kubectl -n prelude logs vco-app-0 -c vco-server-app --tail=200

# logs em arquivo do serviço
ls -la /var/log/services-logs/prelude/vco-app/file-logs/

# buscar a mensagem em todo o histórico rotacionado
find /var/log/services-logs/prelude/vco-app/file-logs/ -type f -print0 \
  | xargs -0 grep -l "Failed to import"
```

- O pod é `vco-app-0`, namespace **`prelude`** (o mesmo nome do tempo do Aria Automation).
- No **embarcado** o `/data/vco` **não** existe: os caminhos `.../data/vco/usr/lib/vco/...`
  que aparecem em KBs de appliance externo servem só para o externo. Os diretórios que sobram
  (`conf/`, `plugins/SQL/`) ficam em `/usr/lib/vco/app-server/`.
- Logs rotacionados são `.xz` — use `xzgrep` em vez de `grep`.
- Cuidado com o nome da pasta: a TechDocs 9.1 escreve **`file-logs`**; a KB 326113 escreve
  **`files-logs`**. Se o `ls` der "No such file", tente a outra — e use `ls /var/log/services-logs/prelude/vco-app/`
  para ver o que existe antes de montar o caminho.
- Fonte de tudo isso: TechDocs 9.1 (Kerberos / plugins, 05/11/2026) e KB 326113 (8.x, mas é a
  mesma estrutura de `services-logs` no 9.1).

---

### 5) Versionamento no Git

O pacote é **binário e gerado**: ele não vai para o repositório. O que vai é o que o gerou.

**Commite:**

- os elementos extraídos — `.action`, `.workflow`, `input_form_*`, `info`: texto, `git diff` normal
- o script separado (`.js`, `.ps1`) quando existir, para revisão de código pura
- um `README.md` por pacote com: versão, `vso-version` de origem, lista de elementos,
  `used-plugins`, pré-requisitos e procedimento de import
- uma **tag** no commit que gerou o pacote (`v13.0.0`), porque o nome do arquivo carrega a versão

**Não commite:** `.package` gerado (nem `.zip`, nem `.b64`), `signatures/`, `certificates/`,
ConfigurationElement com valores reais, `.env`, token, senha.

**Regra de versão:** a versão é do **conjunto**, não do elemento. O vRO versiona elemento por
elemento e o import decide por elemento (por isso o 409 existe). Quem garante que o conjunto é
coerente é o seu repositório: tag + README + lista de elementos. Sem isso, "importa no meu mas
não no cliente" é destino, não azar.

---

### 6) Checklist de entrega (o que o cliente recebe junto com o pacote)

1. `.package` assinado, com nome versionado (`com.cliente.coisa-13.0.0.package`).
2. `README` com `vso-version` de origem e `used-plugins` — para ele saber se o destino tem os plugins.
3. Lista de elementos e o que cada um faz, com o **ponto de entrada** destacado (o workflow que importa).
4. Procedimento de import: **Assets → Packages → Import**, aceitar o certificado do publicador,
   **desmarcar** "Import Configuration Attribute Values".
5. Rollback: reimportar a versão anterior com `overwrite=true` — e o aviso de que isso **não**
   desfaz objeto apagado no destino.
6. Uma linha dizendo **o que não foi testado**. Entrega sem essa linha é promessa, não entrega.

---

### 7) As cicatrizes (erros que custaram tempo de verdade)

| Erro | Causa | Correção |
|---|---|---|
| Pacote recusado, sem mensagem clara | montado à mão / assinatura ausente | exportar do próprio vRO; conferir `contentVerified` |
| Acento vira lixo no import | `data`/`input_form_` em UTF-8 | UTF-16BE **com BOM**; export de Unicode em hex é o sintoma |
| `Exception binding was not set` | item com `catch-name` sem `throw-bind-name` | criar a variável de erro e ligar o *Output exception binding* |
| Senha do cliente sobrescrita no import | "Import Configuration Attribute Values" marcado | desmarcar; `importConfigurationAttributeValues=false` por API |
| Pacote importa, workflow não roda | plugin do `used-plugins` ausente no destino | instalar o plugin antes, ou avisar no README |
| Funciona no 8.x, quebra no 9.1 | `vso-version` de origem antigo demais | abrir o pacote no 9.1 e reexportar — não reusar pacote velho |

---

### Prática (20 min)

Use o workflow do Módulo 11 (ou um dos seus reais) e faça o ciclo completo duas vezes:

1. Crie o pacote no seu vRO com a action e o workflow, **Skip rebuilding**, exporte.
2. Rode o `import-details` e leia os quatro campos. Anexe a resposta ao seu `README.md`.
3. Importe num ambiente/tenant de laboratório, aceitando o certificado.
4. Provogue o **409**: importe de novo a versão anterior. Leia a mensagem — é o gate de versão.
5. Abra o log (`kubectl -n prelude logs vco-app-0 -c vco-server-app --tail=200`) e ache a linha
   do import. Se você não consegue achar o próprio import no log, você não vai achar o do cliente.

**Como saber que funcionou:** o item importado executa no destino, o `README` responde sozinho
as perguntas de pré-requisito, e você sabe dizer onde no log aparece o import daquele arquivo.

---

### Fontes

- TechDocs — Import a Package in VCF Operations orchestrator (15/06/2026). O texto é o mesmo no 9.1;
  este é o endereço que responde hoje (o caminho `/9-1/...` devolve 404 com request direto):
  https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/configuration-of-vmware-cloud-foundation-operations-orchestrator/managing-packages-in-vro/import-a-package-in-the-operations-client.html
- TechDocs 9.1 — Configurar Kerberos nos plugins (caminhos de log do embarcado, `/data/vco` excluído), 05/11/2026:
  https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/configuration-of-vmware-cloud-foundation-operations-orchestrator/vcf-ochestrator-plugins-overview/manage-the-orchestrator-plug-ins/configure-kerberos-authentication.html
- KB 326113 — Services logs locations and pod descriptions (Aria Automation / Orchestrator 8.x):
  https://knowledge.broadcom.com/external/article/326113/services-logs-locations-and-pod-descript.html
- KB 405937 — Importing package in Aria Orchestrator fails with 400 Bad request:
  https://knowledge.broadcom.com/external/article/405937/importing-package-in-aria-orchestrator-f.html
- KB 388745 — Import above 5 min times out (envoy `stream-idle-timeout`, 8.18.1):
  https://knowledge.broadcom.com/external/article/388745/failed-to-import-package-http-failure-re.html
- API — Import Package e Import-details (VCF Operations Orchestrator API 9.1):
  https://developer.broadcom.com/xapis/vcf-operations-orchestrator-api/latest/packages/post
  https://developer.broadcom.com/xapis/vcf-operations-orchestrator-api/latest/packages/import-details/post
- Estrutura interna e algoritmo de assinatura: verificação sobre export real do 9.1.1 em
  11/11/2026 (54/54 entradas reconstruídas, 18/18 assinaturas validadas).

---

## Regras do curso

1. **Um modulo por vez.** Nao pule para Docker sem ter feito um commit.
2. **Erro e material didatico.** Manda o erro inteiro, nao o resumo — o texto do erro diz onde esta.
3. **Nada de assinatura.** Se uma aula pedir cartao, a aula esta errada.
4. **Pergunta boba nao existe**, mas pergunta vaga sim: "nao funciona" nao da para ensinar, "deu erro 403 no push" da.

## Progresso

Marque aqui conforme avanca:

- [ ] Modulo 0 — entender
- [ ] Modulo 1 — Git
- [ ] Modulo 2 — GitHub e push
- [ ] Modulo 3 — Docker
- [ ] Modulo 4 — ai-stack rodando
- [ ] Modulo 5 — acesso remoto
- [ ] Modulo 6 — CI
- [ ] Modulo 7 — GPU
- [ ] Modulo 8 — seguranca
- [ ] Modulo 9 — integracao VCF (partes A e B escritas)
- [ ] Modulo 10 — primeiro caso de uso real (relatorio de VMs por projeto)
- [ ] Modulo 11 — primeiro workflow no vRO (action normalizarNomeVM)
- [ ] Modulo 12 — pacote, assinatura, versionamento e entrega
