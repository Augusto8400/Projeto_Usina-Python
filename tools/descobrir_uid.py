# -*- coding: utf-8 -*-
"""
Utilitário para descobrir o UID de cada tag RFID.

Rode este script na Raspberry (com o leitor MFRC522 já ligado),
encoste cada cubo um de cada vez e anote o UID mostrado. Depois
copie os UIDs para data/rfid_map.json, associando cada um à
partícula correspondente.

Uso:
    python3 tools/descobrir_uid.py
"""
try:
    from mfrc522 import SimpleMFRC522
except ImportError:
    print("Biblioteca 'mfrc522' não encontrada. Instale com:")
    print("  pip install mfrc522 spidev")
    raise SystemExit(1)

reader = SimpleMFRC522()

print("Encoste um cubo no leitor (Ctrl+C para sair)...")
try:
    while True:
        uid, text = reader.read()
        print(f"UID lido: {uid}")
except KeyboardInterrupt:
    print("\nEncerrado.")
