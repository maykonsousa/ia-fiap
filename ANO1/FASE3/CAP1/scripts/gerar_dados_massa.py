"""
Gera producao.csv (CAP6) e sensores.csv (CAP1) relacionados por producao_id.

Uso:
    cd ANO1/FASE3/CAP1
    python3 scripts/gerar_dados_massa.py --count 100
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from dados_fase2 import (
    PRODUCAO_FIELDS,
    SENSORES_FIELDS,
    generate_dataset,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
JSON_PATH = DATA_DIR / "producao_fase2.json"
PRODUCAO_CSV = DATA_DIR / "producao.csv"
SENSORES_CSV = DATA_DIR / "sensores.csv"


def _cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value != value:
        return ""
    return str(value)


def write_csv(producao: list[dict], sensores: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(PRODUCAO_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PRODUCAO_FIELDS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in producao:
            writer.writerow(
                {
                    "id": row["id"],
                    "farm": _cell(row["farm"]),
                    "tons": f"{float(row['tons']):.2f}",
                    "loss_pct": f"{float(row['loss_pct']):.2f}",
                    "harvest_type": _cell(row["harvest_type"]),
                    "created_at": _cell(row["created_at"]),
                }
            )

    with open(SENSORES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SENSORES_FIELDS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in sensores:
            writer.writerow({k: _cell(row[k]) for k in SENSORES_FIELDS})

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(producao, f, indent=4, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera producao (CAP6) e sensores (CAP1) com producao_id em comum."
    )
    parser.add_argument("-n", "--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.count < 1:
        print("Use --count >= 1", file=sys.stderr)
        return 1

    producao, sensores = generate_dataset(args.count, args.seed)
    write_csv(producao, sensores)

    ativa = sum(1 for s in sensores if s["irrigation_status"] == "Ativa")
    print(f"Gerados {args.count} pares producao + sensores (producao_id 1..{args.count})")
    print(f"  CAP6 -> {PRODUCAO_CSV.relative_to(ROOT)}")
    print(f"  CAP1 -> {SENSORES_CSV.relative_to(ROOT)}")
    print(f"  Irrigacao ativa (regra umidade<60 ou NPK): {ativa}/{args.count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
