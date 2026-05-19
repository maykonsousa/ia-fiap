# Dashboards — Programa Ir Além

Três visões dos dados da Fase 2, em **Streamlit** (multipágina) e **Dash** (abas).

## Dashboards

| #   | Arquivo                       | Conteúdo                               |
| --- | ----------------------------- | -------------------------------------- |
| 1   | `pages/1_Campo_e_sensores.py` | Umidade, pH, N/P/K — linguagem simples |
| 2   | `pages/2_Colheita.py`         | Toneladas, perda, prejuízo em R$       |
| 3   | `pages/3_Visao_completa.py`   | Tudo junto + coluna **O que fazer?**   |

## Streamlit (recomendado para o vídeo)

```bash
cd ANO1/FASE3/CAP1
python3 scripts/gerar_dados_massa.py --count 100
pip install -r dashboard/requirements.txt
streamlit run dashboard/Home.py
```

Menu lateral: **Home → Sensores → Produção → Integrado**.

## Dash (alternativa)

```bash
python dashboard/dash_app.py
```

Abre http://127.0.0.1:8050

## Prints

![Consulta 10](../prints/dash_01.png)

![Consulta 10](../prints/dash_02.png)

![Consulta 10](../prints/dash_03.png)

![Consulta 10](../prints/dash_04.png)
