"""Textos e colunas em linguagem acessivel (nao tecnica)."""

from __future__ import annotations

import pandas as pd

COR_IRRIGACAO = {
    "Ativa": "#e74c3c",
    "Desligada": "#27ae60",
    "Ligada": "#e74c3c",
    "Desligada_pt": "#27ae60",
}

ROTULO_IRRIGACAO = {"Ativa": "Ligada", "Desligada": "Desligada"}
ROTULO_COLHEITA = {"manual": "Colheita manual", "mecanizada": "Colheita por maquina"}
ROTULO_NUTRIENTE = {"S": "OK", "N": "Baixo"}


def traduzir_npk(valor: str) -> str:
    return ROTULO_NUTRIENTE.get(str(valor).upper(), str(valor))


def preparar_sensores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Irrigacao"] = out["irrigation_status"].map(ROTULO_IRRIGACAO)
    out["Fazenda"] = out["farm"]
    out["Regiao"] = out["region"]
    out["Umidade do ar (%)"] = out["humidity_pct"]
    out["Acidez do solo (pH)"] = out["soil_pH"]
    out["Temperatura (C)"] = out["temperature"]
    out["Nitrogenio"] = out["nitrogen_ok"].map(traduzir_npk)
    out["Fosforo"] = out["phosphorus_ok"].map(traduzir_npk)
    out["Potassio"] = out["potassium_ok"].map(traduzir_npk)
    out["Adubo"] = out["fertilizer_status"].replace(
        {"Completo": "Nutrientes OK", "Deficitario": "Falta nutriente"}
    )
    return out


def preparar_producao(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Fazenda"] = out["farm"]
    out["Producao (toneladas)"] = out["tons"]
    out["Perda na colheita (%)"] = out["loss_pct"]
    out["Tipo de colheita"] = out["harvest_type"].map(ROTULO_COLHEITA)
    return out


def sugestao_simples(row: pd.Series) -> str:
    """Texto curto para produtor rural."""
    from lib.data import TEMP_ALTA, UMIDADE_MINIMA

    problemas: list[str] = []
    if row["humidity_pct"] < UMIDADE_MINIMA:
        problemas.append("ar muito seco")
    if row["temperature"] >= TEMP_ALTA and row["humidity_pct"] < 65:
        problemas.append("dia quente")
    if row.get("nitrogen_ok") == "N" or row.get("phosphorus_ok") == "N" or row.get("potassium_ok") == "N":
        problemas.append("solo precisa de adubo")

    if row["irrigation_status"] == "Ativa":
        if problemas:
            return "Regar agora — " + ", ".join(problemas)
        return "Regando — situacao sob controle"

    if problemas:
        return "Vale ligar a irrigacao — " + ", ".join(problemas)
    return "Tudo certo — pode manter irrigacao desligada"


def preparar_integrado(df: pd.DataFrame) -> pd.DataFrame:
    out = preparar_sensores(df)
    out = preparar_producao(out)
    out["O que fazer?"] = df.apply(sugestao_simples, axis=1)
    out["Prejuizo estimado (R$)"] = df.apply(
        lambda r: round(r["tons"] * (r["loss_pct"] / 100) * 120, 2), axis=1
    )
    return out
