# -*- coding: utf-8 -*-
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_panel, draw_paragraph, draw_footer_hint
from data.particles_data import ANTIMATTER_PAIRS


class AntimatterScreen(Screen):
    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "ANTIMATÉRIA", self.width // 2, 80, size=36)

        intro = ("Para cada partícula existe uma antipartícula: mesma massa, "
                 "mas propriedades opostas (como carga elétrica). Quando "
                 "matéria e antimatéria se encontram, elas se aniquilam, "
                 "liberando energia pura.")
        y = draw_paragraph(surface, intro, 40, 150, self.width - 80, size=18)

        y += 30
        f_h = theme.font(18)
        for pair in ANTIMATTER_PAIRS:
            rect_h = 70
            from ui.widgets import draw_panel as _dp
            import pygame
            rect = pygame.Rect(40, y, self.width - 80, rect_h)
            draw_panel(surface, rect, border_color=theme.PURPLE, width=2)

            l1 = f_h.render(pair["particle"], True, theme.CYAN)
            l2 = f_h.render("↔", True, theme.GOLD)
            l3 = f_h.render(pair["antiparticle"], True, theme.RED)
            l4 = theme.font(15).render(pair["charge"], True, theme.WHITE)

            surface.blit(l1, (rect.x + 20, rect.y + 12))
            surface.blit(l2, (rect.x + rect.w // 2 - 10, rect.y + 12))
            surface.blit(l3, (rect.x + rect.w // 2 + 20, rect.y + 12))
            surface.blit(l4, (rect.x + 20, rect.y + 40))

            y += rect_h + 16

        draw_footer_hint(surface, self.width, self.height, "B VOLTA AO MENU")
