# -*- coding: utf-8 -*-
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_menu_list, draw_footer_hint

MENU_ITEMS = [
    ("Léptons e Quarks", "leptons_quarks"),
    ("Antimatéria", "antimatter"),
    ("Jogo dos Hádrons", "hadron_game"),
    ("Forças", "forces"),
    ("Spin", "spin"),
    ("Quiz", "quiz"),
]


class HomeScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.selected = 0

    def handle_input(self, action):
        if action == "UP":
            self.selected = (self.selected - 1) % len(MENU_ITEMS)
        elif action == "DOWN":
            self.selected = (self.selected + 1) % len(MENU_ITEMS)
        elif action == "A":
            self.next_screen = MENU_ITEMS[self.selected][1]
        # "B" não faz nada na home (já é a tela raiz)

    def on_cube_placed(self, particle):
        # Encostar qualquer cubo na home já leva direto pro leitor
        self.next_screen = "cube_reader"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "PARTÍCULAS\nELEMENTARES", self.width // 2, 110, size=44)

        f_sub = theme.font(16)
        sub = f_sub.render("ENCOSTE UM CUBO NO LEITOR OU ESCOLHA UMA OPÇÃO", True, theme.CYAN)
        surface.blit(sub, sub.get_rect(center=(self.width // 2, 210)))

        labels = [name for name, _ in MENU_ITEMS]
        list_w = self.width - 100
        draw_menu_list(surface, labels, self.selected, 50, 280, list_w, item_h=80, size=24)

        draw_footer_hint(surface, self.width, self.height,
                          "CIMA/BAIXO NAVEGA · A CONFIRMA")
