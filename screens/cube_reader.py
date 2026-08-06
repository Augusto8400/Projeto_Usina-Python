# -*- coding: utf-8 -*-
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_panel, draw_paragraph, draw_footer_hint


class CubeReaderScreen(Screen):
    """Tela do leitor físico de cubos. Fica esperando um cubo ser
    encostado no sensor RFID e mostra a ficha da partícula."""

    def on_enter(self):
        super().on_enter()
        self.particle = None

    def handle_input(self, action):
        if action == "B":
            self.next_screen = "home"

    def on_cube_placed(self, particle):
        self.particle = particle

    def on_cube_removed(self):
        self.particle = None

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "LEITOR DE CUBOS", self.width // 2, 90, size=34)

        if self.particle is None:
            self._draw_waiting(surface, t)
        else:
            self._draw_particle(surface, self.particle)

        draw_footer_hint(surface, self.width, self.height, "B VOLTA AO MENU")

    def _draw_waiting(self, surface, t):
        import math
        f = theme.font(22)
        pulse = 0.5 + 0.5 * math.sin(t * 3)
        #color = tuple(int(c * pulse + 20) for c in theme.PURPLE)
        color = ( 255, 0, 0)

        cx, cy = self.width // 2, self.height // 2 - 60
        radius = 130
        pygame.draw.circle(surface, color, (cx, cy), radius, 6)
        pygame.draw.circle(surface, theme.PANEL_BG, (cx, cy), radius - 10)

        icon = theme.font(60).render("📡", True, theme.GOLD)
        surface.blit(icon, icon.get_rect(center=(cx, cy)))

        msg = f.render("ENCOSTE UM CUBO", True, theme.WHITE)
        surface.blit(msg, msg.get_rect(center=(self.width // 2, cy + radius + 60)))
        msg2 = f.render("NO LEITOR", True, theme.WHITE)
        surface.blit(msg2, msg2.get_rect(center=(self.width // 2, cy + radius + 100)))

    def _draw_particle(self, surface, p):
        panel = pygame.Rect(40, 150, self.width - 80, self.height - 300)
        draw_panel(surface, panel, border_color=p["color"], width=5)

        name_f = theme.font(38)
        name_img = name_f.render(p["name"], True, p["color"])
        surface.blit(name_img, name_img.get_rect(center=(self.width // 2, panel.y + 60)))

        type_f = theme.font(20)
        type_img = type_f.render(p["type"], True, theme.CYAN)
        surface.blit(type_img, type_img.get_rect(center=(self.width // 2, panel.y + 105)))

        rows = [
            ("Carga", p["charge"]),
            ("Spin", p["spin"]),
            ("Massa", p["mass"]),
        ]
        f_label = theme.font(20)
        f_val = theme.font(20)
        ry = panel.y + 150
        for label, val in rows:
            l_img = f_label.render(f"{label}:", True, theme.GOLD)
            v_img = f_val.render(val, True, theme.WHITE)
            surface.blit(l_img, (panel.x + 30, ry))
            surface.blit(v_img, (panel.x + 200, ry))
            ry += 36

        draw_paragraph(surface, p["description"], panel.x + 30, ry + 20,
                        panel.width - 60, size=18, line_gap=6)
