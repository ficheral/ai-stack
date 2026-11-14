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
- [ ] Modulo 9 — integracao VCF
