# -*- coding: utf-8 -*-
"""
Leitor RFID (MFRC522 via SPI) rodando em thread própria.

Cada cubo do modelo padrão tem uma tag RFID colada com um UID único.
Este módulo fica escutando o leitor continuamente e chama um callback
quando:
  - um cubo novo é encostado no leitor  -> on_cube_placed(uid)
  - o cubo é retirado do leitor         -> on_cube_removed()

Como o MFRC522 não tem detecção contínua de presença (é pergunta e
resposta), consideramos "cubo retirado" quando ficamos
config.RFID_REMOVE_TIMEOUT segundos sem nenhuma leitura bem-sucedida.

Em modo desenvolvimento (sem leitor real conectado / sem biblioteca
mfrc522 instalada), este módulo não faz nada sozinho — no main.py, as
teclas 1-8 simulam encostar cada um dos cubos, chamando os mesmos
callbacks diretamente.
"""
import threading
import time

import config

try:
    from mfrc522 import SimpleMFRC522
    MFRC522_AVAILABLE = True
except Exception:
    MFRC522_AVAILABLE = False


class RFIDReader:
    def __init__(self, on_cube_placed, on_cube_removed):
        """
        on_cube_placed(uid: str)  -- chamado quando um novo UID é detectado
        on_cube_removed()         -- chamado quando o cubo some do leitor
        """
        self.on_cube_placed = on_cube_placed
        self.on_cube_removed = on_cube_removed
        self._current_uid = None
        self._last_seen = 0.0
        self._stop = threading.Event()
        self._thread = None
        self._reader = None

        self.available = MFRC522_AVAILABLE and config.RFID_ENABLED
        if self.available:
            self._reader = SimpleMFRC522()

    def start(self):
        if not self.available:
            print("[rfid] mfrc522 não disponível — leitor físico desativado "
                  "(use as teclas 1-8 para simular cubos).")
            return
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("[rfid] leitor MFRC522 iniciado.")

    def stop(self):
        self._stop.set()

    def _loop(self):
        while not self._stop.is_set():
            try:
                # read_no_block() retorna (None, None) se não achar tag,
                # ou (id, text) se achar. Depende da versão da lib; por
                # segurança tentamos read_no_block e caímos para read
                # com timeout curto se não existir.
                if hasattr(self._reader, "read_no_block"):
                    uid, _text = self._reader.read_no_block()
                else:
                    uid = None
            except Exception as e:
                uid = None

            now = time.time()

            if uid:
                uid = str(uid)
                self._last_seen = now
                if uid != self._current_uid:
                    self._current_uid = uid
                    self.on_cube_placed(uid)
            else:
                if self._current_uid is not None:
                    if now - self._last_seen > config.RFID_REMOVE_TIMEOUT:
                        self._current_uid = None
                        self.on_cube_removed()

            time.sleep(config.RFID_POLL_INTERVAL)
