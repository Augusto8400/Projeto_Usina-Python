# -*- coding: utf-8 -*-
import pygame
import math

from enum import Enum, auto

from screens.base import Screen
from ui import theme
from ui.widgets import (
    draw_background,
    draw_title,
    draw_menu_list,
    draw_footer_hint,
    draw_panel,
    draw_paragraph,
)


MENU_ITEMS = [
    ("Léptons e Quarks", "leptons_quarks"),
    ("Antimatéria", "antimatter"),
    ("Jogo dos Hádrons", "hadron_game"),
    ("Forças", "forces"),
    ("Spin", "spin"),
    ("Quiz", "quiz"),
]


class HomeState(Enum):
    MENU = auto()
    PARTICLE = auto()


class HomeScreen(Screen):

    def on_enter(self):
        super().on_enter()

        self.selected = 0
        self.state = HomeState.MENU
        self.particle = None

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    def handle_input(self, action):

        # Enquanto mostra uma partícula
        if self.state == HomeState.PARTICLE:

            if action == "B":
                self.state = HomeState.MENU
                self.particle = None

            return

        # ---------- MENU ----------

        if action == "UP":
            self.selected = (self.selected - 1) % len(MENU_ITEMS)

        elif action == "DOWN":
            self.selected = (self.selected + 1) % len(MENU_ITEMS)

        elif action == "A":
            self.next_screen = MENU_ITEMS[self.selected][1]

    # --------------------------------------------------------
    # RFID
    # --------------------------------------------------------

    def on_cube_placed(self, particle):
        self.particle = particle
        self.state = HomeState.PARTICLE

    def on_cube_removed(self):
        self.particle = None
        self.state = HomeState.MENU

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def draw(self, surface, t):

        draw_background(surface, self.starfield, t)

        if self.state == HomeState.MENU:
            self._draw_menu(surface,t)

        else:
            self._draw_particle(surface)
    
    # -------------------------------------------------------
    # ANIMATION
    # -------------------------------------------------------
    
    def _draw_rfid_hint(self, surface, t):

        cx = self.width // 2
        y = 210

        # Movimento do cubo
        offset = math.sin(t * 2.5) * 15

        # ---------- Cubo ----------
        cube = pygame.Rect(cx - 120 + offset, y , 40, 40)

        pygame.draw.rect(surface, theme.GOLD, cube, border_radius=4)
        pygame.draw.rect(surface, theme.WHITE, cube, 2, border_radius=4)

        # ---------- Seta ----------
        pygame.draw.line(
            surface,
            theme.CYAN,
            (cx - 65, y + 20),
            (cx - 15, y + 20),
            3,
        )

        pygame.draw.polygon(
            surface,
            theme.CYAN,
            [
                (cx - 15, y + 20),
                (cx - 25, y + 14),
                (cx - 25, y + 26),
            ]
        )

        # ---------- Leitor ----------
        reader = pygame.Rect(cx, y - 10, 90, 60)

        pygame.draw.rect(
            surface,
            theme.PANEL_BG,
            reader,
            border_radius=6,
        )

        pygame.draw.rect(
            surface,
            theme.PURPLE,
            reader,
            3,
            border_radius=6,
        )

        # Luz piscando
        if math.sin(t * 6) > 0:
            led = theme.GREEN
        else:
            led = theme.RED

        pygame.draw.circle(surface, led, (reader.centerx, reader.centery), 6)

        # # Texto
        # text = theme.font(14).render(
        #     "ENCOSTE O CUBO",
        #     True,
        #     theme.CYAN,
        # )

        # surface.blit(
        #     text,
        #     text.get_rect(center=(cx, y + 75))
        # )
        
    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    def _draw_menu(self, surface, t):

        draw_title(
            surface,
            "PARTÍCULAS\nELEMENTARES",
            self.width // 2,
            110,
            size=44,
        )
        
        self._draw_rfid_hint(surface, t)

        f_sub = theme.font(16)

        sub = f_sub.render(
            "ENCOSTE UM CUBO NO LEITOR OU ESCOLHA UMA OPÇÃO",
            True,
            theme.CYAN,
        )

        surface.blit(
            sub,
            sub.get_rect(center=(self.width // 2, 280))
        )

        labels = [name for name, _ in MENU_ITEMS]

        draw_menu_list(
            surface,
            labels,
            self.selected,
            50,
            340,
            self.width - 100,
            item_h=80,
            size=24,
        )

        draw_footer_hint(
            surface,
            self.width,
            self.height - 50,
            "CIMA/BAIXO PARA NAVEGAR • APERTE PARA CONFIRMAR",
        )

    # --------------------------------------------------------
    # PARTÍCULA
    # --------------------------------------------------------

    def _draw_particle(self, surface):

        p = self.particle

        draw_title(
            surface,
            "PARTÍCULA DETECTADA",
            self.width // 2,
            90,
            size=34,
        )

        panel = pygame.Rect(
            40,
            150,
            self.width - 80,
            self.height - 300,
        )

        draw_panel(
            surface,
            panel,
            border_color=p["color"],
            width=5,
        )

        name = theme.font(38).render(
            p["name"],
            True,
            p["color"],
        )

        surface.blit(
            name,
            name.get_rect(center=(self.width // 2, panel.y + 60)),
        )

        kind = theme.font(20).render(
            p["type"],
            True,
            theme.CYAN,
        )

        surface.blit(
            kind,
            kind.get_rect(center=(self.width // 2, panel.y + 105)),
        )

        rows = [
            ("Carga", p["charge"]),
            ("Spin", p["spin"]),
            ("Massa", p["mass"]),
        ]

        y = panel.y + 150

        for label, value in rows:

            l = theme.font(20).render(
                f"{label}:",
                True,
                theme.GOLD,
            )

            v = theme.font(20).render(
                value,
                True,
                theme.WHITE,
            )

            surface.blit(l, (panel.x + 30, y))
            surface.blit(v, (panel.x + 220, y))

            y += 36

        draw_paragraph(
            surface,
            p["description"],
            panel.x + 30,
            y + 20,
            panel.width - 60,
            size=18,
            line_gap=6,
        )

        draw_footer_hint(
            surface,
            self.width,
            self.height - 50,
            "RETIRE O CUBO OU MANTENHA PRESSIONADO",
        )