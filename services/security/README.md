# Seguranca

Ferramentas gratuitas e locais. Nenhuma exige conta ou licenca paga.

| Ferramenta | Licenca | Para que |
|---|---|---|
| Trivy | Apache-2.0 | Vulnerabilidade em dependencia, imagem de container e IaC |
| Semgrep | LGPL-2.1 | Regras de codigo (OWASP) e deteccao de segredo |
| OWASP ZAP | Apache-2.0 | Varredura de aplicacao web |
| Nuclei | MIT | Templates de verificacao |

Uso: `./scan.sh <pasta-do-projeto>`

Nao instale Wazuh/Grafana aqui: eles querem um host inteiro e nao cabem em
2 OCPU / 12 GB junto com o resto. Se um dia precisar, e um host separado.
