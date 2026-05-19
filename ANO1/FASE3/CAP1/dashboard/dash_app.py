"""
Dashboard Dash — versao com textos simples.
    python3 dashboard/dash_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dash
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from lib.data import UMIDADE_MINIMA, load_integrado, load_producao, load_sensores
from lib.labels import preparar_integrado, preparar_producao, preparar_sensores

try:
    sensores = preparar_sensores(load_sensores())
    producao = preparar_producao(load_producao())
    integrado = preparar_integrado(load_integrado())
except FileNotFoundError:
    print("Gere os dados: python3 scripts/gerar_dados_massa.py --count 100")
    raise SystemExit(1)

app: Dash = Dash(__name__, title="FarmTech")
app.layout = html.Div(
    [
        html.H1("🌱 FarmTech — Painel para o produtor"),
        html.P("Escolha uma aba: sensores do campo, colheita ou visão completa."),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Campo e sensores",
                    children=[
                        html.P(f"Umidade ideal acima de {UMIDADE_MINIMA:.0f}%."),
                        dcc.Graph(
                            figure=px.bar(
                                sensores.sort_values("Umidade do ar (%)"),
                                x="Fazenda",
                                y="Umidade do ar (%)",
                                color="Irrigacao",
                            ).add_hline(y=UMIDADE_MINIMA, line_dash="dash")
                        ),
                        dash_table.DataTable(
                            data=sensores[
                                ["Fazenda", "Umidade do ar (%)", "Acidez do solo (pH)", "Nitrogenio", "Fosforo", "Potassio", "Irrigacao"]
                            ].to_dict("records"),
                            page_size=10,
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Colheita",
                    children=[
                        dcc.Graph(
                            figure=px.bar(producao, x="Fazenda", y="Perda na colheita (%)", color="Tipo de colheita")
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Visão completa",
                    children=[
                        dcc.Graph(
                            figure=px.scatter(
                                integrado,
                                x="Temperatura (C)",
                                y="Umidade do ar (%)",
                                color="Irrigacao",
                                hover_name="Fazenda",
                            )
                        ),
                        dash_table.DataTable(
                            data=integrado[
                                ["Fazenda", "Perda na colheita (%)", "Irrigacao", "O que fazer?"]
                            ].head(15).to_dict("records"),
                            page_size=10,
                        ),
                    ],
                ),
            ]
        ),
    ],
    style={"fontFamily": "Arial, sans-serif", "margin": "24px", "maxWidth": "1200px"},
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
