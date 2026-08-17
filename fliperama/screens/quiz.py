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

        q = self._question()
        draw_title(surface, "QUIZ", self.width // 2, 70, size=32)

        f_prog = theme.font(16)
        prog = f_prog.render(f"Pergunta {self.q_index + 1}/{len(QUIZ_QUESTIONS)}  ·  Pontos: {self.score}",
                              True, theme.CYAN)
        surface.blit(prog, prog.get_rect(center=(self.width // 2, 120)))

        draw_paragraph(surface, q["question"], 40, 160, self.width - 80, size=20)

        list_y = 320
        draw_menu_list(surface, q["options"], self.selected, 50, list_y, self.width - 100,
                        item_h=70, size=20)

        if self.answered:
            correct = self.selected == q["correct"]
            panel = pygame.Rect(40, list_y + len(q["options"]) * 86 + 10, self.width - 80, 220)
            border = theme.GREEN if correct else theme.RED
            draw_panel(surface, panel, border_color=border, width=4)
            f_res = theme.font(22)
            msg = "✓ CORRETO!" if correct else "✗ ERRADO!"
            msg_img = f_res.render(msg, True, border)
            surface.blit(msg_img, (panel.x + 20, panel.y + 16))
            draw_paragraph(surface, q["explanation"], panel.x + 20, panel.y + 56,
                            panel.width - 40, size=16)
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
