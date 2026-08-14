# -*- coding: utf-8 -*-
"""
Leitor RFID MFRC522 via SPI.

Este módulo lê SOMENTE o UID da tag.

Não realiza:
    - autenticação MIFARE;
    - leitura de blocos;
    - escrita;
    - leitura de memória da tag.

Isso é suficiente para o projeto, pois cada cubo é identificado
exclusivamente pelo UID da sua tag RFID.
"""

import threading
import time

import config

try:
    from mfrc522 import MFRC522

    MFRC522_AVAILABLE = True

except Exception as e:
    MFRC522_AVAILABLE = False
    print(f"[rfid] Erro ao importar MFRC522: {e}")


class RFIDReader:

    def __init__(self, on_cube_placed, on_cube_removed):

        self.on_cube_placed = on_cube_placed
        self.on_cube_removed = on_cube_removed

        self._current_uid = None
        self._last_seen = 0.0

        self._stop = threading.Event()
        self._thread = None

        self._reader = None

        self.available = (
            MFRC522_AVAILABLE
            and config.RFID_ENABLED
        )

        if self.available:

            try:
                self._reader = MFRC522()
                print("[rfid] MFRC522 configurado.")

            except Exception as e:
                print(
                    f"[rfid] Erro ao inicializar MFRC522: {e}"
                )

                self.available = False

    # =========================================================
    # INICIAR
    # =========================================================

    def start(self):

        if not self.available:

            print(
                "[rfid] Leitor físico desativado "
                "(use as teclas 1-8 para simular cubos)."
            )

            return

        self._stop.clear()

        self._thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self._thread.start()

        print("[rfid] Leitor MFRC522 iniciado.")

    # =========================================================
    # PARAR
    # =========================================================

    def stop(self):

        self._stop.set()

        if self._thread is not None:

            self._thread.join(timeout=1.0)

        print("[rfid] Leitor MFRC522 parado.")

    # =========================================================
    # LOOP DO LEITOR
    # =========================================================

    def _loop(self):

        while not self._stop.is_set():

            uid = None

            try:

                # -------------------------------------------------
                # 1. Verifica se existe uma tag próxima
                # -------------------------------------------------

                status, _ = self._reader.MFRC522_Request(
                    self._reader.PICC_REQIDL
                )

                if status == self._reader.MI_OK:

                    # -------------------------------------------------
                    # 2. Executa anticollision
                    #
                    # Isso obtém o UID da tag.
                    #
                    # IMPORTANTE:
                    # Não fazemos MFRC522_Auth aqui.
                    # -------------------------------------------------

                    status, uid_data = (
                        self._reader.MFRC522_Anticoll()
                    )

                    if status == self._reader.MI_OK:

                        uid = self._format_uid(uid_data)

            except Exception:
                # Falhas momentâneas de comunicação não devem
                # derrubar a thread do leitor.
                uid = None

            now = time.time()

            # =====================================================
            # TAG DETECTADA
            # =====================================================

            if uid:

                self._last_seen = now

                # Só dispara o callback quando o UID muda.
                if uid != self._current_uid:

                    self._current_uid = uid

                    print(
                        f"[rfid] UID detectado: {uid}"
                    )

                    self.on_cube_placed(uid)

            # =====================================================
            # TAG NÃO DETECTADA
            # =====================================================

            else:

                if self._current_uid is not None:

                    elapsed = (
                        now - self._last_seen
                    )

                    if elapsed > config.RFID_REMOVE_TIMEOUT:

                        print(
                            "[rfid] Tag removida: "
                            f"{self._current_uid}"
                        )

                        self._current_uid = None

                        self.on_cube_removed()

            time.sleep(
                config.RFID_POLL_INTERVAL
            )

    # =========================================================
    # CONVERTER UID
    # =========================================================

    @staticmethod
    def _format_uid(uid_data):

        if not uid_data:
            return None

        try:

            # A biblioteca normalmente retorna uma lista
            # contendo os bytes do UID + BCC.
            #
            # O BCC não faz parte do UID.
            #
            # Para UID de 4 bytes:
            #   [58, 55, 14, 59, 20]
            #
            # usamos:
            #   585514
            #
            # Entretanto, mantemos o comportamento compatível
            # com o formato que seu programa já estava recebendo.

            uid_bytes = list(uid_data)

            # Remove o BCC quando houver 5 bytes.
            if len(uid_bytes) == 5:
                uid_bytes = uid_bytes[:4]

            return "".join(
                str(int(byte))
                for byte in uid_bytes
            )

        except Exception:
            return None