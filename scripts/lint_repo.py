#!/usr/bin/env python3
"""Verificacoes do repositorio, rodadas no CI e local.

Uso:
    python3 scripts/lint_repo.py            # valida YAML
    python3 scripts/lint_repo.py --exec-bit # scripts .sh com bit +x no Git

Exit 1 se algo falhar, com o nome do arquivo e o que corrigir.
"""
from __future__ import annotations

import glob
import subprocess
import sys

try:
    import yaml
except ImportError:
    print("falta pyyaml: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)


def check_yaml() -> int:
    padroes = ["compose/*.yml", "compose/*.yaml",
               ".github/workflows/*.yml", ".github/workflows/*.yaml"]
    arquivos: list[str] = []
    for p in padroes:
        arquivos.extend(sorted(glob.glob(p)))

    if not arquivos:
        print("nenhum YAML encontrado")
        return 0

    falhou = 0
    for f in arquivos:
        try:
            yaml.safe_load(open(f, encoding="utf-8"))
            print(f"ok   {f}")
        except Exception as e:
            print(f"FAIL {f}: {e}")
            falhou = 1
    return falhou


def check_exec_bit() -> int:
    """Todo .sh versionado precisa estar 100755, senao 'Permission denied'."""
    scripts = sorted(set(glob.glob("scripts/*.sh") + glob.glob("services/*/*.sh")))
    if not scripts:
        print("nenhum .sh encontrado")
        return 0

    falhou = 0
    for s in scripts:
        try:
            saida = subprocess.run(
                ["git", "ls-files", "-s", s],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"AVISO {s}: nao esta no Git ainda")
            continue

        if not saida:
            print(f"AVISO {s}: fora do controle de versao")
            continue

        modo = saida.split()[0]
        if modo == "100755":
            print(f"ok   {s} (executavel)")
        else:
            print(f"FAIL {s}: modo {modo}, deveria ser 100755")
            print(f"     corrija: git update-index --chmod=+x {s}")
            falhou = 1
    return falhou


def main() -> int:
    if "--exec-bit" in sys.argv:
        return check_exec_bit()
    return check_yaml()


if __name__ == "__main__":
    raise SystemExit(main())
