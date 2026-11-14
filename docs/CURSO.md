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

---

## Módulo 9 — parte A: do VCF Automation para fora

*Escrito pelo professor VCF 9.1.x.*

### Fluxo de autenticação (9.x)

Não existe mais login programático com usuário/senha. O caminho é:

1. Você cria um **API token** na UI (My Account → API Tokens, ~90 dias).
2. Troca esse token por um **bearer access token** (~1h de validade).
3. Usa `Authorization: Bearer` em todas as chamadas.

O endpoint da troca depende do plano/instalação:

| Plano | Endpoint |
|---|---|
| Provider / All Apps (instância nova, sem org VM Apps) | `POST /oauth/provider/token` |
| Org VM Apps | `POST /tm/oauth/tenant/<org>/token`, `grant_type=refresh_token` |
| VCF 9.1 unificado (VIDB) | `POST https://<vidb>/acs/t/<role>/token` com `api_token=` |
| Org herdada do Aria 8.x | `/csp/gateway/am/api/login.json` + `POST /iaas/api/login` |

### Embarcado × externo

O Automation do domínio de gestão é instância nova, quase sempre **sem org VM Apps**
→ caminho provider. Instância externa ou herdada de 8.x mantém a org →
`/tm/oauth/tenant/...`. Confira a org no Provider Portal → Organizations antes de
escrever código.

### Credencial nunca no código

`export VCFA_API_TOKEN=...`, `.env` no `.gitignore`, secret no CI,
`env_file`/`secrets:` no compose. Se um token foi commitado: **rotacione**, não
apague o commit e finja que resolveu.

```bash
export VCFA_HOST=vcfa.exemplo.com VCFA_TENANT=minha-org
TOKEN=$(curl -sk -X POST "https://$VCFA_HOST/tm/oauth/tenant/$VCFA_TENANT/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d grant_type=refresh_token -d "refresh_token=$VCFA_API_TOKEN" | jq -r .access_token)
curl -sk "https://$VCFA_HOST/iaas/api/projects" -H "Authorization: Bearer $TOKEN" | jq .
```

No plano provider, liste `/cloudapi/1.0.0/orgs` — *confirme na doc*.

### Os 3 primeiros erros

| Código | Causa | O que significa |
|---|---|---|
| **401** | Mandou o API token como Bearer | Ele só serve para gerar o access token |
| **404 / redirect** | Org ou plano errado | Provider × tenant, ou org inexistente |
| **403** | Token bom, papel insuficiente | Permissão na org, não autenticação |

### Ajuste para o seu ambiente (TJSP)

O TJSP é **9.1.1 embarcado** e tem org de tenant **TJSP-VMs** (VM Apps), então o
caminho que se aplica é `/tm/oauth/tenant/TJSP-VMs/token`.

**Ressalva que eu marco:** o professor descreve o caminho *provider* usando API
token, mas o que já observamos na prática é que **o menu de API Tokens aparece na
org de tenant**, não no provider. Os dois relatos não fecham. Antes de escrever
código, abra a sua instância e confirme de onde o token sai — não presuma. Se o
menu de API Tokens estiver só na org, o caminho provider da tabela acima não se
aplica ao seu caso.

*Fonte citada: TechDocs 9.1 — "Get Your Access Token for the VCF Automation API",
"Generating API Tokens for Service Provider Account", "OAuth Token Support for API
and CLI Access" (VIDB).*

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

## Módulo 11 — seu primeiro workflow de verdade (30 min)

**Prática:** uma action ES5 que normaliza nome de VM + um workflow que a chama.
Acento e espaço em nome de VM quebram hostname, pasta de datastore e tag.

### 1) Criar a action

Inventário → **Actions** → nova pasta `com.tjsp.aula` → *Add Action* → nome `normalizarNomeVM`.
Aba **Script**: colar o código. Aba **Inputs**: `nome`, tipo `string`. **Return type**: `string`.

```js
// ES5 / Rhino — sem let, const, arrow, template string
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

### 3) O que você deve ver

- Log: `Nome normalizado: servidor-acao-c` — e o output `nomeNormalizado` igual.
- Com `nomeVM` vazio: o workflow falha com *Informe o nome da VM.* (a exceção da action sobe para o workflow — é o que você quer).
- Com `!!!`: falha com *Nome inválido*.

**O que acabou de acontecer:** a action é a função, o workflow é quem a orquestra.
O binding IN é o argumento, o OUT é o `return`. Sem OUT ligado, a action roda e o valor se perde — erro silencioso mais comum.

*Versão:* `System.getModule` existe de 7.x a 9.1. Em 9.x o Rhino continua o motor padrão de actions (ES5). `throw` em action aparece como erro do workflow; usar `WorkflowException` também é válido.

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
- [ ] Modulo 10 — primeiro caso de uso real de VCF
- [ ] Modulo 11 — primeiro workflow no vRO
