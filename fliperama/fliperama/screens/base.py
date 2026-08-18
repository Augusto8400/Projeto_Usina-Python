# -*- coding: utf-8 -*-
"""Classe base para todas as telas do fliperama."""
from ui.widgets import Starfield


class Screen:
    """
    Cada tela implementa:
      - on_enter()                 chamado ao entrar na tela
      - handle_input(action)       action é "UP"/"DOWN"/"LEFT"/"RIGHT"/"A"/"B"
      - on_cube_placed(particle)   partícula (dict) encostada no leitor RFID
      - on_cube_removed()          cubo retirado do leitor
      - update(dt)
      - draw(surface, t)

    Para navegar, defina self.next_screen = "nome_da_tela" (ver
    NAV_MAP em main.py) e o loop principal troca de tela no próximo
    frame.
    """

    def __init__(self, app):
        self.app = app          # referência ao App (main.py) p/ navegação e dados
        self.width = app.width
        self.height = app.height
        self.starfield = Starfield(self.width, self.height)
        self.next_screen = None

    def on_enter(self):
        self.next_screen = None

    def handle_input(self, action):
        if action == "B":
            self.next_screen = "home"

    def on_cube_placed(self, particle):
        pass

    def on_cube_removed(self):
        pass

    def update(self, dt):
        pass

    def draw(self, surface, t):
        pass
