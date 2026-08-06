# -*- coding: utf-8 -*-
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title, draw_menu_list, draw_paragraph, draw_footer_hint, draw_panel
from data.particles_data import QUIZ_QUESTIONS


class QuizScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.q_index = 0
        self.selected = 0
        self.answered = False
        self.score = 0
        self.finished = False

    def _question(self):
        return QUIZ_QUESTIONS[self.q_index]

    def handle_input(self, action):
        if self.finished:
            if action == "A":
                self.on_enter()  # reinicia
            elif action == "B":
                self.next_screen = "home"
            return

        q = self._question()
        if not self.answered:
            if action == "UP":
                self.selected = (self.selected - 1) % len(q["options"])
            elif action == "DOWN":
                self.selected = (self.selected + 1) % len(q["options"])
            elif action == "A":
                self.answered = True
                if self.selected == q["correct"]:
                    self.score += 1
            elif action == "B":
                self.next_screen = "home"
        else:
            if action == "A":
                self.q_index += 1
                self.selected = 0
                self.answered = False
                if self.q_index >= len(QUIZ_QUESTIONS):
                    self.finished = True
            elif action == "B":
                self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)

        if self.finished:
            self._draw_result(surface)
            return

        # escala com base no menor lado da tela, pra funcionar tanto em
        # telas verticais (TV) quanto horizontais (monitor de teste)
        s = min(self.width, self.height) / 900

        q = self._question()
        title_size = max(20, int(32 * s))
        draw_title(surface, "QUIZ", self.width // 2, int(self.height * 0.07), size=title_size)

        f_prog = theme.font(max(12, int(16 * s)))
        prog = f_prog.render(f"Pergunta {self.q_index + 1}/{len(QUIZ_QUESTIONS)}  ·  Pontos: {self.score}",
                              True, theme.CYAN)
        prog_y = int(self.height * 0.13)
        surface.blit(prog, prog.get_rect(center=(self.width // 2, prog_y)))

        q_start_y = int(self.height * 0.18)
        y_after_question = draw_paragraph(surface, q["question"], 40, q_start_y,
                                           self.width - 80, size=max(14, int(20 * s)))

        list_y = y_after_question + 30
        item_h = max(44, int(70 * s))
        n_opts = len(q["options"])

        # espaço restante disponível até o rodapé, pra decidir se cabe
        # o painel de feedback abaixo da lista sem cortar
        footer_reserve = 50
        list_bottom = list_y + n_opts * (item_h + 16)

        draw_menu_list(surface, q["options"], self.selected, 50, list_y, self.width - 100,
                        item_h=item_h, size=max(14, int(20 * s)))

        if self.answered:
            correct = self.selected == q["correct"]
            panel_y = list_bottom + 10
            panel_h = max(120, self.height - panel_y - footer_reserve)
            panel = pygame.Rect(40, panel_y, self.width - 80, panel_h)
            border = theme.GREEN if correct else theme.RED
            draw_panel(surface, panel, border_color=border, width=4)
            f_res = theme.font(max(16, int(22 * s)))
            msg = "✓ CORRETO!" if correct else "✗ ERRADO!"
            msg_img = f_res.render(msg, True, border)
            surface.blit(msg_img, (panel.x + 20, panel.y + 12))
            draw_paragraph(surface, q["explanation"], panel.x + 20, panel.y + 48,
                            panel.width - 40, size=max(12, int(16 * s)))
            draw_footer_hint(surface, self.width, self.height, "A PARA PRÓXIMA · B VOLTA")
        else:
            draw_footer_hint(surface, self.width, self.height,
                              "CIMA/BAIXO ESCOLHE · A CONFIRMA")

    def _draw_result(self, surface):
        draw_title(surface, "RESULTADO", self.width // 2, 150, size=36)

        f = theme.font(30)
        score_img = f.render(f"{self.score} / {len(QUIZ_QUESTIONS)}", True, theme.GOLD)
        surface.blit(score_img, score_img.get_rect(center=(self.width // 2, self.height // 2 - 40)))

        pct = self.score / len(QUIZ_QUESTIONS)
        if pct == 1:
            msg = "PERFEITO! Você é um físico de partículas!"
        elif pct >= 0.6:
            msg = "Muito bem! Continue estudando."
        else:
            msg = "Explore as outras telas e tente de novo!"
        draw_paragraph(surface, msg, 60, self.height // 2 + 20, self.width - 120,
                        size=18, color=theme.CYAN)

        draw_footer_hint(surface, self.width, self.height, "A JOGA DE NOVO · B VOLTA AO MENU")
