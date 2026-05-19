"""
Gera amostra pequena (5 registros) usando a mesma logica de dados_fase2.py.

Uso:
    cd ANO1/FASE3/CAP1
    python3 scripts/gerar_csv.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gerar_dados_massa import write_csv
from dados_fase2 import generate_dataset


def main() -> None:
    producao, sensores = generate_dataset(5, seed=42)
    write_csv(producao, sensores)
    print("Amostra: 5 pares producao + sensores em data/")


if __name__ == "__main__":
    main()
