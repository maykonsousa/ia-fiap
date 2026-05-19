# Conexão entre os projetos da Fase 2 e Fase 3

Este capítulo (**CAP1**) e o **CAP6** fazem parte do mesmo domínio (agronegócio / cana-de-açúcar) e se complementam na **Fase 3**.

## Visão geral

| Entrega | Pasta | O que faz | Tipo de dado |
|---------|-------|-----------|--------------|
| Irrigação IoT | `FASE2/CAP1` (este) | ESP32 + sensores DHT22/LDR, relé de irrigação | Leituras de **campo** (umidade, pH simulado, NPK) |
| Produção e perdas | `FASE2/CAP6` | Sistema CLI + Oracle | **Cadastros** do produtor (toneladas, perda %, colheita) |
| Banco Oracle | `FASE3/CAP1` | Importação CSV + consultas SQL | `sensores` + `producao` no Oracle FIAP |

## Sensores do hardware → colunas do banco (Fase 3)

| No projeto IoT (CAP1) | No CSV / tabela `sensores` (Fase 3) |
|-----------------------|--------------------------------------|
| DHT22 — umidade | `soil_moisture` / `humidity_pct` |
| DHT22 — temperatura | `temperature` |
| LDR — simulação de pH | `soil_pH` |
| Botões NPK | `fertilizer_type` (Organico / Misto / Inorganico) |
| Relé de irrigação | `irrigation_type` (Gotejamento / Aspersao / Nenhum / Manual) |
| — | `region`, `crop_type`, `rainfall_mm`, `sunlight_hours` (complemento do dataset FIAP) |

Na Fase 3, o arquivo `data/sensores.csv` segue o **formato pedido pela disciplina** (exemplo `Sensores_Fazenda.csv`), inspirado nas leituras que este firmware envia pela serial.

## Fluxo sugerido para documentar na entrega

1. **CAP1** — demonstrar o circuito e leituras no Monitor Serial (umidade, pH, irrigação).
2. **CAP6** — cadastrar lotes de colheita na aplicação Python.
3. **FASE3/CAP1** — importar `data/sensores.csv` (e opcionalmente `data/producao.csv`) no Oracle e rodar `sql/03_consultas.sql`.

## Integrantes (mesmo grupo)

- Heleno Madeira — RM570302  
- Samantha Silva Farias — RM574120  
- Matheus de França Fantini — RM574078  
- Maykon Eduardo Pereira de Sousa — RM574011  
