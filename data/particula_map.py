# -*- coding: utf-8 -*-
"""
Carrega o mapeamento das partículas.

O particle_mapping.json é a fonte única de configuração.

Cada partícula possui:
    - UID da tag RFID
    - índices das seções da fita LED
"""

import json
import os


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------

_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "particula_map.json"
)


with open(_JSON_PATH, "r", encoding="utf-8") as f:
    _raw = json.load(f)


# ---------------------------------------------------------------------------
# Mapeamento completo
# ---------------------------------------------------------------------------

PARTICLE_MAPPING = {
    nome: dados
    for nome, dados in _raw.items()
    if not nome.startswith("_")
}


# ---------------------------------------------------------------------------
# UID -> partícula
# ---------------------------------------------------------------------------

RFID_MAP = {
    str(dados["uid"]): nome
    for nome, dados in PARTICLE_MAPPING.items()
}


# ---------------------------------------------------------------------------
# Partícula -> LEDs
# ---------------------------------------------------------------------------

LED_MAPPING = {
    nome: dados["leds"]
    for nome, dados in PARTICLE_MAPPING.items()
}


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def get_particle_by_uid(uid):
    """
    Recebe um UID RFID e retorna o nome da partícula.

    Exemplo:
        get_particle_by_uid("122913161392")
        -> "foton"
    """

    return RFID_MAP.get(str(uid))


def get_leds(nome):
    """
    Recebe o nome da partícula e retorna os índices
    das duas seções da fita.

    Exemplo:
        get_leds("foton")
        -> [10, 18]
    """

    return LED_MAPPING.get(nome)