"""Painel do campo — sensores."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import plotly.express as px
import streamlit as st
from lib.data import UMIDADE_MINIMA, load_sensores
from lib.labels import COR_IRRIGACAO, preparar_sensores

st.set_page_config(page_title="Campo e sensores", layout="wide")
st.title("📡 Como está o campo agora?")
st.markdown("Leituras dos **sensores na plantação** (umidade, solo e irrigação).")

try:
    raw = load_sensores()
except FileNotFoundError:
    st.error("Dados não encontrados. Peça ao suporte técnico para gerar os arquivos.")
    st.stop()

df = preparar_sensores(raw)

st.sidebar.header("Filtrar")
regiao = st.sidebar.multiselect("Região", sorted(df["Regiao"].unique()), default=sorted(df["Regiao"].unique()))
irr = st.sidebar.multiselect(
    "Irrigação",
    ["Ligada", "Desligada"],
    default=["Ligada", "Desligada"],
)
f = df[df["Regiao"].isin(regiao) & df["Irrigacao"].isin(irr)]

ligadas = int((f["Irrigacao"] == "Ligada").sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Fazendas", len(f))
c2.metric("Umidade média", f"{f['Umidade do ar (%)'].mean():.0f}%", help="Quanto o ar está úmido")
c3.metric("Solo (pH médio)", f"{f['Acidez do solo (pH)'].mean():.1f}", help="5,5 a 6,5 é uma faixa boa")
c4.metric("Regando agora", ligadas, help="Quantas fazendas com irrigação ligada")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Umidade do ar em cada fazenda")
    st.caption(f"Linha tracejada = mínimo recomendado (**{UMIDADE_MINIMA:.0f}%**)")

    fig = px.bar(
        f.sort_values("Umidade do ar (%)"),
        x="Fazenda",
        y="Umidade do ar (%)",
        color="Irrigacao",
        color_discrete_map={"Ligada": COR_IRRIGACAO["Ativa"], "Desligada": COR_IRRIGACAO["Desligada"]},
        labels={"Irrigacao": "Irrigação"},
    )
    fig.add_hline(y=UMIDADE_MINIMA, line_dash="dash", annotation_text="Mínimo 60%")
    fig.update_layout(showlegend=True, legend_title_text="Irrigação")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Irrigação ligada ou desligada")
    st.plotly_chart(
        px.pie(f, names="Irrigacao", color="Irrigacao", color_discrete_map={
            "Ligada": COR_IRRIGACAO["Ativa"],
            "Desligada": COR_IRRIGACAO["Desligada"],
        }),
        use_container_width=True,
    )

st.subheader("Adubo no solo (N, P e K)")
st.caption("**N** = nitrogênio · **P** = fósforo · **K** = potássio · **OK** = nível bom · **Baixo** = precisa atenção")

st.dataframe(
    f[["Fazenda", "Regiao", "Nitrogenio", "Fosforo", "Potassio", "Adubo", "Irrigacao"]],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Resumo visual: umidade × acidez do solo")
st.plotly_chart(
    px.scatter(
        f,
        x="Umidade do ar (%)",
        y="Acidez do solo (pH)",
        color="Irrigacao",
        size="Temperatura (C)",
        hover_name="Fazenda",
        color_discrete_map={"Ligada": COR_IRRIGACAO["Ativa"], "Desligada": COR_IRRIGACAO["Desligada"]},
    ),
    use_container_width=True,
)
