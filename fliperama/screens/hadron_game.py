# -*- coding: utf-8 -*-
import random
import time
import pygame
from collections import Counter

from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_panel, draw_footer_hint
from data.particles_data import AVAILABLE_QUARKS, HADRONS


class HadronGameScreen(Screen):
    """
    Minigame: monta hádrons combinando quarks (e antiquarks).

    Controles:
      ESQ/DIR  -> navega pela paleta de quarks disponíveis
      A        -> adiciona o quark selecionado à combinação atual (máx. 3)
      B        -> remove o último quark adicionado (ou volta ao menu se
                   a combinação estiver vazia)
      CIMA     -> confere a combinação contra o hádron-alvo
      DOWN     -> limpa a combinação atual

    Corrigido em relação ao app original: agora a checagem funciona
    também para mésons (2 quarks, com antiquark), não só bárions.
    """

    def on_enter(self):
        super().on_enter()
        self.palette_index = 0
        self.selected = []          # lista de dicts de AVAILABLE_QUARKS
        self.score = 0
        self.attempts = 0
        self.feedback = ""
        self.feedback_color = theme.WHITE
        self.feedback_until = 0
        self.target = None
        self._new_target()

    def _new_target(self):
        self.target = random.choice(HADRONS)
        self.selected = []
        self.feedback = ""

    def handle_input(self, action):
        now = time.time()
        # enquanto mostra feedback de acerto/erro, qualquer botão avança
        if self.feedback and now < self.feedback_until:
            return

        if action == "LEFT":
            self.palette_index = (self.palette_index - 1) % len(AVAILABLE_QUARKS)
        elif action == "RIGHT":
            self.palette_index = (self.palette_index + 1) % len(AVAILABLE_QUARKS)
        elif action == "A":
            if len(self.selected) < 3:
                self.selected.append(AVAILABLE_QUARKS[self.palette_index])
                self.feedback = ""
        elif action == "B":
            if self.selected:
                self.selected.pop()
                self.feedback = ""
            else:
                self.next_screen = "home"
        elif action == "DOWN":
            self.selected = []
            self.feedback = ""
        elif action == "UP":
            self._check_combination()

    def _check_combination(self):
        if not self.selected:
            return
        self.attempts += 1

        symbols = [q["symbol"] for q in self.selected]
        total_charge = sum(q["charge"] for q in self.selected)

        # Comparação por contagem de símbolos, funciona para bárions
        # (3 quarks) e mésons (quark + antiquark) igualmente.
        if Counter(symbols) == Counter(self.target["quarks"]):
            self.feedback = f"✓ CORRETO! Você criou: {self.target['name'].upper()}!"
            self.feedback_color = theme.GREEN
            self.score += 10
            self.feedback_until = time.time() + 1.8
            self._pending_new_target = True
        else:
            self._pending_new_target = False
            if abs(total_charge - self.target["charge"]) < 0.01:
                self.feedback = f"Carga certa ({total_charge:.2f}), mas combinação errada!"
            else:
                self.feedback = f"✗ Errado! Carga: {total_charge:.2f} (esperado: {self.target['charge']})"
            self.feedback_color = theme.RED
            self.feedback_until = time.time() + 1.8

    def update(self, dt):
        if self.feedback and time.time() >= self.feedback_until:
            if getattr(self, "_pending_new_target", False):
                self._new_target()
            self.feedback = ""

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        draw_title(surface, "JOGO DOS HÁDRONS", self.width // 2, 60, size=26)

        f_small = theme.font(16)
        info = f_small.render(f"Pontos: {self.score}   Tentativas: {self.attempts}", True, theme.CYAN)
        surface.blit(info, info.get_rect(center=(self.width // 2, 105)))

        # alvo
        target_panel = pygame.Rect(40, 130, self.width - 80, 80)
        draw_panel(surface, target_panel, border_color=theme.GOLD, width=3)
        f_t = theme.font(24)
        t_img = f_t.render(f"ALVO: {self.target['name']}  (carga {self.target['charge']:+d})",
                            True, theme.GOLD)
        surface.blit(t_img, t_img.get_rect(center=target_panel.center))

        # combinação atual
        combo_panel = pygame.Rect(40, 230, self.width - 80, 110)
        draw_panel(surface, combo_panel, border_color=theme.PURPLE, width=2)
        f_c = theme.font(30)
        slot_w = combo_panel.width // 3
        for i in range(3):
            slot_rect = pygame.Rect(combo_panel.x + i * slot_w, combo_panel.y, slot_w, combo_panel.height)
            pygame.draw.rect(surface, theme.PURPLE, slot_rect, 1)
            if i < len(self.selected):
                q = self.selected[i]
                img = f_c.render(q["symbol"], True, q["color"])
                surface.blit(img, img.get_rect(center=slot_rect.center))

        # paleta de quarks (navegável)
        pal_y = 370
        f_p = theme.font(20)
        pal_label = f_p.render("PALETA DE QUARKS (ESQ/DIR navega, A adiciona)", True, theme.WHITE)
        surface.blit(pal_label, (40, pal_y))

        item_w = (self.width - 80) // len(AVAILABLE_QUARKS)
        for i, q in enumerate(AVAILABLE_QUARKS):
            rect = pygame.Rect(40 + i * item_w, pal_y + 40, item_w - 8, 70)
            is_sel = i == self.palette_index
            border = theme.GOLD if is_sel else q["color"]
            draw_panel(surface, rect, border_color=border, width=4 if is_sel else 2)
            img = theme.font(26).render(q["symbol"], True, q["color"])
            surface.blit(img, img.get_rect(center=(rect.centerx, rect.centery - 8)))
            small = theme.font(12).render(q["name"], True, theme.WHITE)
            surface.blit(small, small.get_rect(center=(rect.centerx, rect.centery + 22)))

        # feedback
        if self.feedback:
            fb_panel = pygame.Rect(40, pal_y + 130, self.width - 80, 90)
            draw_panel(surface, fb_panel, border_color=self.feedback_color, width=4)
            fb_img = theme.font(18).render(self.feedback, True, self.feedback_color)
            surface.blit(fb_img, fb_img.get_rect(center=fb_panel.center))

        draw_footer_hint(surface, self.width, self.height,
                          "CIMA CONFERE · BAIXO LIMPA · B REMOVE/VOLTA")
