# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_panel, draw_paragraph, draw_footer_hint

TEXT = (
    "Spin é uma propriedade quântica intrínseca das partículas, algo "
    "como um \"momento angular interno\". Não é literalmente a partícula "
    "girando, mas se comporta matematicamente de forma parecida.\n\n"
    "Partículas de matéria (léptons e quarks) têm spin 1/2 — são "
    "chamadas de férmions. Partículas mediadoras de força (fóton, "
    "glúon, bósons W/Z) têm spin 1 — são os bósons. O bóson de Higgs "
    "é especial: tem spin 0."
)


class SpinScreen(Screen):
    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "SPIN", self.width // 2, 90, size=40)

        # ícone girando
        cx, cy = self.width // 2, 220
        r = 50
        angle = t * 180
        end = (cx + r * math.cos(math.radians(angle)), cy + r * math.sin(math.radians(angle)))
        pygame.draw.circle(surface, theme.PANEL_BG, (cx, cy), r)
        pygame.draw.circle(surface, theme.GOLD, (cx, cy), r, 4)
        pygame.draw.line(surface, theme.GOLD, (cx, cy), end, 4)

        panel = pygame.Rect(40, 300, self.width - 80, self.height - 420)
        draw_panel(surface, panel)
        draw_paragraph(surface, TEXT, panel.x + 24, panel.y + 24, panel.width - 48, size=18)

        draw_footer_hint(surface, self.width, self.height, "B VOLTA AO MENU")
