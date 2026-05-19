"""Painel da colheita."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import plotly.express as px
import streamlit as st
from lib.data import load_producao, prejuizo_brl
from lib.labels import ROTULO_COLHEITA, preparar_producao

st.set_page_config(page_title="Colheita", layout="wide")
st.title("🌾 Como foi a colheita?")
st.markdown("Quanto saiu do campo, **quanto se perdeu** e o **prejuízo em reais**.")

try:
    raw = load_producao().copy()
except FileNotFoundError:
    st.error("Dados não encontrados.")
    st.stop()

raw["prejuizo_brl"] = raw.apply(lambda r: prejuizo_brl(r["tons"], r["loss_pct"]), axis=1)
df = preparar_producao(raw)
df["Prejuizo (R$)"] = raw["prejuizo_brl"]

tipos = sorted(df["Tipo de colheita"].unique())
tipo_sel = st.sidebar.multiselect("Tipo de colheita", tipos, default=tipos)
f = df[df["Tipo de colheita"].isin(tipo_sel)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Fazendas", len(f))
c2.metric("Cana colhida", f"{f['Producao (toneladas)'].sum():,.0f} t")
c3.metric("Perda média", f"{f['Perda na colheita (%)'].mean():.1f}%", help="% que não virou produto")
c4.metric("Prejuízo total", f"R$ {f['Prejuizo (R$)'].sum():,.0f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Perda em cada fazenda (%)")
    st.caption("Quanto maior a barra, mais cana ficou no campo")
    st.plotly_chart(
        px.bar(
            f.sort_values("Perda na colheita (%)", ascending=False),
            x="Fazenda",
            y="Perda na colheita (%)",
            color="Tipo de colheita",
        ),
        use_container_width=True,
    )
with col2:
    st.subheader("Manual x máquina")
    st.caption("Comparar perda entre tipos de colheita")
    inv = {v: k for k, v in ROTULO_COLHEITA.items()}
    box_df = f.copy()
    box_df["harvest_type"] = box_df["Tipo de colheita"].map(inv)
    st.plotly_chart(
        px.box(box_df, x="harvest_type", y="loss_pct", color="harvest_type", labels={
            "harvest_type": "Tipo",
            "loss_pct": "Perda (%)",
        }),
        use_container_width=True,
    )

st.subheader("Onde o prejuízo foi maior?")
st.dataframe(
    f[["Fazenda", "Producao (toneladas)", "Perda na colheita (%)", "Tipo de colheita", "Prejuizo (R$)"]]
    .sort_values("Prejuizo (R$)", ascending=False),
    use_container_width=True,
    hide_index=True,
)
