# Codigo

Scripts reutilizaveis. Regra: cada script com cabecalho dizendo o que faz,
o que precisa instalado e como se chama.

- `vcf/` — helpers de VCF Automation / Orchestrator (o que ja usamos no dia a dia)
- `k8s/` — manifests e helpers
- `win/` — PowerShell

Nada de segredo em arquivo: usar variavel de ambiente ou o GitHub Actions Secret.

## relatorio_vms.py

Relatorio de VMs por projeto no VCF Automation (org VM Apps). So leitura: faz
GET, nunca escreve no ambiente.

```bash
set -a; . ./compose/.env; set +a
python3 services/code/relatorio_vms.py --mes 2026-11
```

Saida em `reports/AAAA-MM/`: `vms-por-projeto.md` e `.csv` (`;`, Excel pt-BR).

Variaveis: `VCFA_HOST`, `VCFA_TENANT` (ex. TJSP-VMs), `VCFA_API_TOKEN`.
Explicacao completa no Modulo 10 de `docs/CURSO.md`.
