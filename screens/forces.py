# -*- coding: utf-8 -*-
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_panel, draw_paragraph, draw_footer_hint
from data.particles_data import FORCES
import pygame


class ForcesScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.index = 0

    def handle_input(self, action):
        if action == "LEFT":
            self.index = (self.index - 1) % len(FORCES)
        elif action == "RIGHT":
            self.index = (self.index + 1) % len(FORCES)
        elif action == "B":
            self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "AS 4 FORÇAS\nFUNDAMENTAIS", self.width // 2, 90, size=30)

        force = FORCES[self.index]
        panel = pygame.Rect(40, 250, self.width - 80, self.height - 420)
        draw_panel(surface, panel, border_color=theme.GOLD, width=4)

        f_name = theme.font(28)
        name_img = f_name.render(force["name"], True, theme.GOLD)
        surface.blit(name_img, name_img.get_rect(center=(self.width // 2, panel.y + 50)))

        f_carrier = theme.font(18)
        carrier_img = f_carrier.render(f"Mediador: {force['carrier']}", True, theme.CYAN)
        surface.blit(carrier_img, carrier_img.get_rect(center=(self.width // 2, panel.y + 90)))

        draw_paragraph(surface, force["description"], panel.x + 24, panel.y + 130,
                        panel.width - 48, size=18)

        # indicador de posição (1 de 4, 2 de 4...)
        dots_y = panel.y + panel.height + 30
        for i in range(len(FORCES)):
            cx = self.width // 2 + (i - (len(FORCES) - 1) / 2) * 30
            color = theme.GOLD if i == self.index else theme.PURPLE
            pygame.draw.circle(surface, color, (int(cx), dots_y), 8)

        draw_footer_hint(surface, self.width, self.height,
                          "ESQ/DIR NAVEGA · B VOLTA")
