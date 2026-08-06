# -*- coding: utf-8 -*-
"""
Leitura do joystick analógico (2 eixos, via MCP3008) e do botão único.

- Mover o stick pra qualquer direção gera um evento lógico "UP"/"DOWN"/
  "LEFT"/"RIGHT" (um evento por movimento -- o stick precisa voltar pro
  centro antes de disparar a mesma direção de novo, como um botão).
- Toque curto no botão = "A" (confirmar). Segurar o botão por mais que
  config.LONG_PRESS_SECONDS = "B" (voltar).

Se gpiozero não estiver disponível (ex.: rodando no PC), cai automatica-
mente para o teclado do pygame, permitindo testar toda a interface sem
hardware nenhum.
"""
import queue
from functools import partial

try:
    from gpiozero import Button as GPIOButton
    GPIOZERO_AVAILABLE = True
except Exception:
    GPIOZERO_AVAILABLE = False

import pygame
import config

# Nomes lógicos usados pelo resto do programa
UP, DOWN, LEFT, RIGHT, A, B = "UP", "DOWN", "LEFT", "RIGHT", "A", "B"

KEYBOARD_MAP = { # Utilizado para o Computador 
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
    sem se importar se veio do joystick+botão físicos ou do teclado.
    """

    def __init__(self):
        self.events = queue.Queue()
        self.using_gpio = GPIOZERO_AVAILABLE

        self._button = None
        self._button_long_fired = False
        
        self._joy_direction = None  # direção "presa" atualmente (None = centro)
        
        self._joy_buttons = {}
        
        if self.using_gpio:
            self._setup_gpio()

    def _setup_gpio(self):

        self._setup_button()
        self._setup_joystick()

        print("GPIO inicializado.")
        
    def _setup_button(self):

        self._button = GPIOButton(
            config.PIN_BUTTON,
            pull_up=True,
            bounce_time=0.05,
            hold_time=config.LONG_PRESS_SECONDS,
            hold_repeat=False,
        )

        self._button.when_pressed = self._on_button_pressed
        self._button.when_held = self._on_button_held
        self._button.when_released = self._on_button_released
    # -- botão --
    def _on_button_pressed(self):
        self._button_long_fired = False

    def _on_button_held(self):
        self._button_long_fired = True
        self.events.put(B)

    def _on_button_released(self):
        if not self._button_long_fired:
            self.events.put(A)

    # -- joystick (chamado a cada frame pelo main.py) --
    def _setup_joystick(self):

        buttons = {
            UP: config.BTN_CIMA,
            DOWN: config.BTN_BAIXO,
            LEFT: config.BTN_ESQUERDA,
            RIGHT: config.BTN_DIREITA,
        }

        for direction, pin in buttons.items():

            button = GPIOButton(
                pin,
                pull_up=True,
                bounce_time=0.05,
            )

            button.when_pressed = partial(
                self._on_joy_pressed,
                direction,
            )

            button.when_released = partial(
                self._on_joy_released,
                direction,
            )

            self._joy_buttons[direction] = button
        
    def _on_joy_pressed(self, direction):

        # Já existe uma direção ativa?
        if self._joy_direction is not None:
            return

        self._joy_direction = direction
        self.events.put(direction)

    def _on_joy_released(self, direction):

        if self._joy_direction == direction:
            self._joy_direction = None


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
