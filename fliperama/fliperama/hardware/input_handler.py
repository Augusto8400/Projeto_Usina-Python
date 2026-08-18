# -*- coding: utf-8 -*-
"""
Leitura dos botões físicos (cima/baixo/esquerda/direita/A/B).

Usa gpiozero quando disponível (Raspberry Pi real). Se não estiver
disponível (ex.: rodando no PC para testar), cai automaticamente para
o teclado do pygame, permitindo testar toda a interface sem hardware.
"""
import queue

try:
    from gpiozero import Button as GPIOButton
    GPIOZERO_AVAILABLE = True
except Exception:
    GPIOZERO_AVAILABLE = False

import pygame
import config

# Nomes lógicos usados pelo resto do programa
UP, DOWN, LEFT, RIGHT, A, B = "UP", "DOWN", "LEFT", "RIGHT", "A", "B"

KEYBOARD_MAP = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_RETURN: A,
    pygame.K_SPACE: A,
    pygame.K_ESCAPE: B,
    pygame.K_BACKSPACE: B,
}


class InputHandler:
    """
    Produz uma fila (queue) de eventos lógicos: "UP", "DOWN", "LEFT",
    "RIGHT", "A", "B". O loop principal do jogo só consome dessa fila,
    sem se importar se veio do GPIO ou do teclado.
    """

    def __init__(self):
        self.events = queue.Queue()
        self.using_gpio = GPIOZERO_AVAILABLE
        self._gpio_buttons = []

        if self.using_gpio:
            self._setup_gpio()

    def _setup_gpio(self):
        pin_map = {
            UP: config.PIN_UP,
            DOWN: config.PIN_DOWN,
            LEFT: config.PIN_LEFT,
            RIGHT: config.PIN_RIGHT,
            A: config.PIN_A,
            B: config.PIN_B,
        }
        for name, pin in pin_map.items():
            btn = GPIOButton(pin, pull_up=True, bounce_time=0.05)
            # closure para capturar "name" corretamente
            btn.when_pressed = (lambda n=name: self.events.put(n))
            self._gpio_buttons.append(btn)
        print("[input] gpiozero conectado — usando botões físicos.")

    def poll_pygame_events(self, pygame_events):
        """Chame isto a cada frame passando pygame.event.get().
        Se estivermos em modo teclado (sem GPIO), converte teclas em
        eventos lógicos. Sempre retorna os eventos brutos do pygame
        também, para permitir tratar QUIT etc. no chamador."""
        if not self.using_gpio:
            for ev in pygame_events:
                if ev.type == pygame.KEYDOWN and ev.key in KEYBOARD_MAP:
                    self.events.put(KEYBOARD_MAP[ev.key])
        return pygame_events

    def get_nowait(self):
        """Retorna o próximo evento lógico pendente, ou None."""
        try:
            return self.events.get_nowait()
        except queue.Empty:
            return None
