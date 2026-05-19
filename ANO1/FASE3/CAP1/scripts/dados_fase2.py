"""
Geracao de producao (CAP6) e sensores (CAP1) com relacao 1:1 por producao_id.

CAP1 - irrigacao-inteligente.ino:
  - DHT22: umidade (%) e temperatura (C)
  - LDR: valor analogico (simula pH)
  - Botoes N, P, K
  - Rele: irrigacao se umidade < 60% ou algum nutriente BAIXO

CAP6 - main.py:
  - farm, tons, loss_pct, harvest_type, created_at
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

# --- CAP1 (firmware) ---
UMIDADE_LIMITE_IRRIGACAO = 60.0
LDR_MIN = 150
LDR_MAX = 4000
LDR_PH_MIN = 5.0
LDR_PH_MAX = 7.0

# --- CAP6 (dominio) ---
MANUAL_LOSS_RANGE = (2.5, 7.5)
MECHANICAL_LOSS_RANGE = (9.0, 22.0)
REGIONS = [
    "Oeste SP",
    "Norte SP",
    "Ribeirao Preto SP",
    "Centro-Oeste SP",
    "Sul de MG",
]
FARM_PREFIXES = ["Fazenda", "Usina", "Cooperativa", "Sitio"]

PRODUCAO_FIELDS = ["id", "farm", "tons", "loss_pct", "harvest_type", "created_at"]

SENSORES_FIELDS = [
    "farm_id",
    "producao_id",
    "farm",
    "crop_type",
    "region",
    "humidity_pct",
    "soil_moisture",
    "ldr_raw",
    "soil_pH",
    "temperature",
    "nitrogen_ok",
    "phosphorus_ok",
    "potassium_ok",
    "fertilizer_status",
    "irrigation_status",
    "recorded_at",
]


def farm_name(index: int) -> str:
    prefix = FARM_PREFIXES[index % len(FARM_PREFIXES)]
    return f"{prefix} {index:03d}"


def farm_id_str(index: int) -> str:
    return f"FARM{index:04d}"


def ldr_to_soil_ph(ldr: int) -> float:
    """Converte leitura LDR (CAP1) para escala de pH usada no relatorio."""
    ratio = (ldr - LDR_MIN) / (LDR_MAX - LDR_MIN)
    ratio = max(0.0, min(1.0, ratio))
    return round(LDR_PH_MIN + ratio * (LDR_PH_MAX - LDR_PH_MIN), 2)


def irrigation_status(humidity: float, n: bool, p: bool, k: bool) -> str:
    """Mesma regra do .ino: rele HIGH se umidade < 60 ou NPK insuficiente."""
    if humidity < UMIDADE_LIMITE_IRRIGACAO or not (n and p and k):
        return "Ativa"
    return "Desligada"


def fertilizer_status(n: bool, p: bool, k: bool) -> str:
    return "Completo" if (n and p and k) else "Deficitario"


def simulate_cap1_reading(rng: random.Random, *, loss_pct: float) -> dict:
    """
    Simula uma leitura do loop do ESP32.
    Perda alta (colheita estressada) tende a umidade um pouco menor.
    """
    bias = (float(loss_pct) - 10.0) / 15.0
    humidity = round(rng.uniform(42, 88) - bias * 8, 2)
    humidity = max(35.0, min(90.0, humidity))

    temperature = round(rng.uniform(24, 38) - (humidity - 60) * 0.05, 2)
    ldr = rng.randint(LDR_MIN, LDR_MAX)

    n = rng.random() > 0.25
    p = rng.random() > 0.25
    k = rng.random() > 0.25

    return {
        "humidity_pct": humidity,
        "soil_moisture": humidity,
        "ldr_raw": ldr,
        "soil_pH": ldr_to_soil_ph(ldr),
        "temperature": temperature,
        "nitrogen_ok": "S" if n else "N",
        "phosphorus_ok": "S" if p else "N",
        "potassium_ok": "S" if k else "N",
        "fertilizer_status": fertilizer_status(n, p, k),
        "irrigation_status": irrigation_status(humidity, n, p, k),
    }


def generate_producao_row(
    rng: random.Random, index: int, base_date: datetime
) -> dict:
    """Um lote cadastrado no sistema CAP6."""
    harvest_type = rng.choice(["manual", "manual", "mecanizada", "mecanizada"])
    if harvest_type == "manual":
        loss_pct = round(rng.uniform(*MANUAL_LOSS_RANGE), 2)
    else:
        loss_pct = round(rng.uniform(*MECHANICAL_LOSS_RANGE), 2)

    created_at = base_date + timedelta(
        days=rng.randint(0, 60),
        hours=rng.randint(0, 10),
        minutes=rng.randint(0, 59),
    )

    return {
        "id": index,
        "farm": farm_name(index),
        "tons": round(rng.uniform(5_000, 32_000), 2),
        "loss_pct": loss_pct,
        "harvest_type": harvest_type,
        "created_at": created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def generate_sensor_row(
    rng: random.Random, producao: dict, region: str
) -> dict:
    """Leitura CAP1 no mesmo talhao/momento do lote de producao."""
    reading = simulate_cap1_reading(rng, loss_pct=float(producao["loss_pct"]))
    pid = int(producao["id"])

    return {
        "farm_id": farm_id_str(pid),
        "producao_id": pid,
        "farm": producao["farm"],
        "crop_type": "Cana-de-acucar",
        "region": region,
        "recorded_at": producao["created_at"],
        **reading,
    }


def generate_dataset(count: int, seed: int) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed)
    base_date = datetime(2026, 4, 1, 8, 0, 0)
    producao: list[dict] = []
    sensores: list[dict] = []

    for i in range(1, count + 1):
        prod = generate_producao_row(rng, i, base_date)
        region = REGIONS[i % len(REGIONS)]
        sensor = generate_sensor_row(rng, prod, region)
        producao.append(prod)
        sensores.append(sensor)

    return producao, sensores
