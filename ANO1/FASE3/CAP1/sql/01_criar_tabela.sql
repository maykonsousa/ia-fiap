-- Modelagem opcional (constraints PK/FK/CHECK) — ver README seção 7.4.
-- O fluxo principal usa o wizard "Importar Dados" do SQL Developer, que cria
-- as tabelas automaticamente a partir dos CSVs. Este script é uma alternativa
-- caso se queira a modelagem com integridade referencial declarada.

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE SENSORS CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE PRODUCTION CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

-- CAP6: cadastro de colheita
-- Observacao: created_at usa VARCHAR2 (nao TIMESTAMP) porque o wizard
-- "Importar Dados" do SQL Developer nao parseia o separador "T" do ISO 8601
-- presente no CSV (ex.: "2026-04-18T11:14:00") quando o destino e TIMESTAMP.
-- Como nenhuma das 10 consultas usa este campo, mante-lo como string evita
-- o erro GDK-05058 sem perda de informacao.
CREATE TABLE PRODUCTION (
    id            NUMBER        NOT NULL PRIMARY KEY,
    farm          VARCHAR2(100) NOT NULL,
    tons          NUMBER(12, 2) NOT NULL,
    loss_pct      NUMBER(5, 2)  NOT NULL,
    harvest_type  VARCHAR2(20)  NOT NULL,
    created_at    VARCHAR2(25)
);

-- CAP1: leituras DHT22, LDR, NPK e status do rele
-- Observacao: recorded_at usa VARCHAR2 pelo mesmo motivo de created_at acima.
CREATE TABLE SENSORS (
    farm_id            VARCHAR2(10) PRIMARY KEY,
    producao_id        NUMBER NOT NULL,
    farm               VARCHAR2(100) NOT NULL,
    crop_type          VARCHAR2(30)  NOT NULL,
    region             VARCHAR2(50)  NOT NULL,
    humidity_pct       NUMBER(5, 2)  NOT NULL,
    soil_moisture      NUMBER(5, 2)  NOT NULL,
    ldr_raw            NUMBER(6, 0)  NOT NULL,
    soil_pH            NUMBER(4, 2)  NOT NULL,
    temperature        NUMBER(5, 2)  NOT NULL,
    nitrogen_ok        CHAR(1)       NOT NULL,
    phosphorus_ok      CHAR(1)       NOT NULL,
    potassium_ok       CHAR(1)       NOT NULL,
    fertilizer_status  VARCHAR2(20)  NOT NULL,
    irrigation_status  VARCHAR2(20)  NOT NULL,
    recorded_at        VARCHAR2(25),
    CONSTRAINT fk_sensors_production
        FOREIGN KEY (producao_id) REFERENCES PRODUCTION (id),
    CONSTRAINT chk_nitrogen CHECK (nitrogen_ok IN ('S', 'N')),
    CONSTRAINT chk_phosphorus CHECK (phosphorus_ok IN ('S', 'N')),
    CONSTRAINT chk_potassium CHECK (potassium_ok IN ('S', 'N'))
);

COMMENT ON TABLE PRODUCTION IS 'FASE2 CAP6 - lotes de colheita';
COMMENT ON TABLE SENSORS IS 'FASE2 CAP1 - leituras IoT por talhao (1:1 com PRODUCTION via producao_id)';

COMMIT;
