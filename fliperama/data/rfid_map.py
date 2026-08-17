# -*- coding: utf-8 -*-
"""Carrega o mapeamento UID da tag RFID -> chave da partícula.

Edite o arquivo data/rfid_map.json (não este .py) para cadastrar os
UIDs reais dos seus cubos. Use tools/descobrir_uid.py para descobrir
o UID de cada tag.
"""
import json
import os

_JSON_PATH = os.path.join(os.path.dirname(__file__), "rfid_map.json")

with open(_JSON_PATH, "r", encoding="utf-8") as f:
    _raw = json.load(f)

# remove chaves de comentário (começam com "_")
RFID_MAP = {k: v for k, v in _raw.items() if not k.startswith("_")}
