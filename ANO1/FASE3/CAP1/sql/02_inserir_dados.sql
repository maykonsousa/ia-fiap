-- Recomendado: importar data/producao.csv e data/sensores.csv pelo SQL Developer
-- (Assistente de Importacao). Os CSV sao gerados por:
--   python3 scripts/gerar_csv.py
--   python3 scripts/gerar_dados_massa.py --count 500

DELETE FROM SENSORS;
DELETE FROM PRODUCTION;

COMMIT;

-- Apos importar os CSV, valide:
SELECT 'PRODUCTION' AS tabela, COUNT(*) AS total FROM PRODUCTION
UNION ALL
SELECT 'SENSORS', COUNT(*) FROM SENSORS;

-- Cada linha de SENSORS deve ter producao_id existente em PRODUCTION:
SELECT s.producao_id, s.farm, p.farm AS farm_producao
FROM SENSORS s
LEFT JOIN PRODUCTION p ON p.id = s.producao_id
WHERE p.id IS NULL;
