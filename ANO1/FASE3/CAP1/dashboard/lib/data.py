"""Carregamento e regras compartilhadas (Streamlit + Dash)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

UMIDADE_MINIMA = 60.0
PH_IDEAL_MIN = 5.5
PH_IDEAL_MAX = 6.5
TEMP_ALTA = 32.0
PRECO_TONELADA_BRL = 120.0


def load_sensores() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "sensores.csv")
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])
    return df


def load_producao() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "producao.csv")


def load_integrado() -> pd.DataFrame:
    s = load_sensores()
    p = load_producao()
    return s.merge(p, left_on="producao_id", right_on="id", suffixes=("", "_prod"))


def sugestao_irrigacao(row: pd.Series) -> str:
    from lib.labels import sugestao_simples

    return sugestao_simples(row)


def prejuizo_brl(tons: float, loss_pct: float) -> float:
    return tons * (loss_pct / 100) * PRECO_TONELADA_BRL
