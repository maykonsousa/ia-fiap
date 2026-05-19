"""Visao completa + recomendacoes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import plotly.express as px
import streamlit as st
from lib.data import TEMP_ALTA, UMIDADE_MINIMA, load_integrado
from lib.labels import COR_IRRIGACAO, preparar_integrado

st.set_page_config(page_title="Visao completa", layout="wide")
st.title("🔗 Visão completa da fazenda")
st.markdown("Junta **colheita** + **sensores** e sugere **se deve regar**.")

try:
    raw = load_integrado()
except FileNotFoundError:
    st.error("Dados não encontrados.")
    st.stop()

df = preparar_integrado(raw)

farm = st.sidebar.selectbox("Ver uma fazenda", ["Todas"] + sorted(df["Fazenda"].unique()))
f = df if farm == "Todas" else df[df["Fazenda"] == farm]

st.subheader("Clima no momento da leitura")
st.caption(
    f"Cada bolha é uma fazenda. **Abaixo de {UMIDADE_MINIMA:.0f}%** de umidade ou **acima de {TEMP_ALTA:.0f}°C** "
    "com ar seco costuma pedir mais atenção na irrigação."
)

fig = px.scatter(
    f,
    x="Temperatura (C)",
    y="Umidade do ar (%)",
    color="Irrigacao",
    symbol="Tipo de colheita",
    size="Perda na colheita (%)",
    hover_name="Fazenda",
    color_discrete_map={"Ligada": COR_IRRIGACAO["Ativa"], "Desligada": COR_IRRIGACAO["Desligada"]},
    labels={"Irrigacao": "Irrigação"},
)
fig.add_hline(y=UMIDADE_MINIMA, line_dash="dot", annotation_text="Umidade mínima")
fig.add_vline(x=TEMP_ALTA, line_dash="dot", annotation_text="Calor alto")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Tabela resumo — o que fazer em cada fazenda")
st.dataframe(
    f[
        [
            "Fazenda",
            "Producao (toneladas)",
            "Perda na colheita (%)",
            "Tipo de colheita",
            "Umidade do ar (%)",
            "Acidez do solo (pH)",
            "Irrigacao",
            "O que fazer?",
            "Prejuizo estimado (R$)",
        ]
    ].sort_values("Perda na colheita (%)", ascending=False),
    use_container_width=True,
    hide_index=True,
)

alertas = f[f["O que fazer?"].str.contains("ligar|Regar", case=False, na=False)]
if len(alertas):
    st.warning(f"⚠️ **{len(alertas)}** fazenda(s) precisam de atenção na irrigação — veja a coluna **O que fazer?**")
else:
    st.success("✅ Nenhuma fazenda com alerta urgente no filtro atual.")
