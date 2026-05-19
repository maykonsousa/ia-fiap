"""Pagina inicial — linguagem simples."""

import streamlit as st

st.set_page_config(page_title="FarmTech", page_icon="🌱", layout="wide")

st.title("🌱 Painel FarmTech — Cana-de-acucar")
st.markdown(
    """
Este painel ajuda o **produtor** a enxergar a fazenda de forma clara — sem termos técnicos.

Escolha uma tela no **menu à esquerda**:
"""
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 📡 Campo e sensores")
    st.write("Umidade do ar, acidez do solo, adubo (N, P, K) e se a **irrigação está ligada**.")
with c2:
    st.markdown("### 🌾 Colheita")
    st.write("Quanto foi colhido, **quanto se perdeu** e se a colheita foi **manual ou por máquina**.")
with c3:
    st.markdown("### 🔗 Visão completa")
    st.write("Junta colheita + sensores e diz **o que fazer** (regar ou não).")

with st.expander("Como ler os números?"):
    st.markdown(
        """
- **Umidade do ar:** quanto o ar está úmido (ideal acima de **60%** para a cana).
- **pH do solo:** acidez (faixa boa entre **5,5 e 6,5**).
- **N, P, K:** nitrogênio, fósforo e potássio — **OK** ou **Baixo**.
- **Irrigação ligada:** o sistema está regando agora.
- **Perda na colheita:** parte da cana que não entrou no caminhão.
"""
    )
