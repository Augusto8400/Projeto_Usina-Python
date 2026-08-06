# -*- coding: utf-8 -*-
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_table, draw_footer_hint
from data.particles_data import LEPTONS, QUARKS


class LeptonsQuarksScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.tab = 0  # 0 = léptons, 1 = quarks

    def handle_input(self, action):
        if action in ("LEFT", "RIGHT"):
            self.tab = 1 - self.tab
        elif action == "B":
            self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "LÉPTONS E QUARKS", self.width // 2, 80, size=32)

        tabs = ["LÉPTONS", "QUARKS"]
        f = theme.font(22)
        for i, label in enumerate(tabs):
            x = self.width // 2 + (i - 0.5) * 220
            color = theme.GOLD if i == self.tab else theme.PURPLE
            img = f.render(("[ " if i == self.tab else "  ") + label + (" ]" if i == self.tab else ""), True, color)
            surface.blit(img, img.get_rect(center=(x, 150)))

        if self.tab == 0:
            headers = ["Partícula", "Carga", "Massa", "Ger."]
            rows = [(l["name"], l["charge"], l["mass"], l["generation"]) for l in LEPTONS]
        else:
            headers = ["Partícula", "Carga", "Massa", "Ger."]
            rows = [((q["name"], q["color"]), q["charge"], q["mass"], q["generation"]) for q in QUARKS]

        col_widths = [int(self.width * 0.42), int(self.width * 0.20),
                      int(self.width * 0.22), int(self.width * 0.16)]
        draw_table(surface, headers, rows, 40, 210, col_widths, size=18, row_h=52)

        draw_footer_hint(surface, self.width, self.height,
                          "ESQ/DIR TROCA ABA · B VOLTA")
