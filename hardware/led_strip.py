# -*- coding: utf-8 -*-

import time

from rpi_ws281x import PixelStrip, Color

import config 
from data.particula_map import LED_MAPPING


class LEDStrip:

    def __init__(self):
        """
        Controlador da fita LED.

        O mapping das partículas é carregado através
        do LED_MAPPING, que vem do arquivo JSON.
        """

        self.strip = PixelStrip(
            config.LED_COUNT,
            config.LED_PIN,
            config.LED_FREQ_HZ,
            config.LED_DMA,
            config.LED_INVERT,
            config.LED_BRIGHTNESS,
            config.LED_CHANNEL
        )

        self.strip.begin()

        print(
            f"[LED] Fita inicializada: "
            f"{config.LED_COUNT} LEDs no GPIO {config.LED_PIN}"
        )

    # -------------------------------------------------
    # ACENDER PARTÍCULA
    # -------------------------------------------------

    
    def show(self, nome, r, g, b):

        if nome not in LED_MAPPING:
            print(f"[LED] Partícula '{nome}' não encontrada.")
            return

        particula = LED_MAPPING[nome]

        print(
            f"[LED] {nome}: "
            f"mapping {particula}"
        )

        for inicio in particula:

            inicio = inicio * config.LED_SECTION

            for offset in range(config.LED_SECTION):

                led = inicio + offset

                if led >= config.LED_COUNT:
                    continue

                self.strip.setPixelColor(
                    led,
                    Color(r, g, b)
                )

        self.strip.show()

    # -------------------------------------------------
    # APAGAR FITA
    # -------------------------------------------------

    def clear(self):
        """
        Apaga todos os LEDs da fita.
        """

        for i in range(config.LED_COUNT):
            self.strip.setPixelColor(
                i,
                Color(0, 0, 0)
            )

        self.strip.show()

    # -------------------------------------------------
    # DESLIGAR
    # -------------------------------------------------

    def stop(self):
        """
        Apaga a fita antes de finalizar o programa.
        """

        self.clear()

        print("[LED] Fita desligada.")