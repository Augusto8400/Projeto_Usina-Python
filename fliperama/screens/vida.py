# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title

class VidaScreen(Screen):
    def on_enter(self):
        super().on_enter()

    def handle_input(self, action):
        if action == "B":
            self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        
        is_landscape = self.width > self.height
        active_w = int(self.height * 0.5625) if is_landscape else self.width
        offset_x = (self.width - active_w) // 2
        center_x = offset_x + (active_w // 2)

        title_y = int(self.height * 0.035)
        draw_title(surface, "TEMPO DE VIDA", center_x, title_y, size=int(active_w * 0.075))

        ctrl_y = title_y + int(self.height * 0.04)
        f_ctrl = theme.font(int(active_w * 0.03))
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)
        
        total_w = 24 + 10 + btn_b_txt.get_width() 
        start_ctrl_x = center_x - (total_w // 2)
        
        pygame.draw.circle(surface, (220, 0, 0), (start_ctrl_x + 12, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (start_ctrl_x + 12, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (start_ctrl_x + 34, ctrl_y - 2))

        # ANIMAÇÃO SUPERIOR (Contagem Regressiva e Instabilidade)
        anim1_box_y = ctrl_y + int(self.height * 0.035)
        anim1_box_h = int(self.height * 0.14) 
        anim1_box_w = active_w - int(active_w * 0.16)
        anim_box_x = offset_x + int(active_w * 0.08)

        anim1_rect = pygame.Rect(anim_box_x, anim1_box_y, anim1_box_w, anim1_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim1_rect, border_radius=15)
        pygame.draw.rect(surface, (255, 100, 200), anim1_rect, width=3, border_radius=15)

        self._draw_timer_animation(surface, t, center_x, anim1_box_y + anim1_box_h//2, active_w)

        # TEXTO DIDÁTICO
        texto_box_y = anim1_box_y + anim1_box_h + int(self.height * 0.015)
        
        paragrafos = [
            "No mundo microscópico, nem tudo dura para sempre. O Tempo de Vida é literalmente o cronômetro natural que diz quanto tempo uma partícula consegue existir antes de desaparecer e se transformar em outra coisa.",
            "A natureza é preguiçosa: ela prefere estados leves e relaxados. Por isso, partículas pesadas (como o Múon ou o Bóson de Higgs) são muito estressadas e instáveis. Elas 'decaem' e explodem em partículas mais leves em uma mera fração de segundo.",
            "As únicas partículas verdadeiramente pacíficas e estáveis do universo são os Elétrons e os Quarks Up e Down (que formam os prótons e nêutrons). É por isso que você, as estrelas e os planetas são feitos inteiramente deles!"
        ]
        
        f_texto = theme.font(int(active_w * 0.027)) 
        padding_topo = int(self.height * 0.02)
        altura_texto_total = padding_topo
        
        for p in paragrafos:
            altura_texto_total += self._get_text_height(p, anim1_box_w - 60, f_texto)
            altura_texto_total += int(self.height * 0.015) 
            
        altura_texto_total += int(self.height * 0.005)
        texto_box_h = altura_texto_total
        
        texto_rect = pygame.Rect(anim_box_x, texto_box_y, anim1_box_w, texto_box_h)
        pygame.draw.rect(surface, (15, 20, 30), texto_rect, border_radius=15)
        pygame.draw.rect(surface, (255, 100, 200), texto_rect, width=3, border_radius=15)
        
        cursor_y = texto_box_y + padding_topo 
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, anim_box_x + 30, cursor_y, anim1_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.015) 

        # ANIMAÇÃO INFERIOR (O Decaimento)
        anim2_box_y = texto_box_y + texto_box_h + int(self.height * 0.015)
        menu_y_home = int(self.height * 0.19)
        item_h_home = int(self.height * 0.045)
        cube_y_home = menu_y_home + (4 * item_h_home) + int(self.height * 0.05)
        cube_h_home = int(active_w * 0.8)
        base_home_y = cube_y_home + cube_h_home
        
        anim2_box_h = base_home_y - anim2_box_y
        if anim2_box_h < int(self.height * 0.12):
            anim2_box_h = int(self.height * 0.12)

        anim2_rect = pygame.Rect(anim_box_x, anim2_box_y, anim1_box_w, anim2_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim2_rect, border_radius=15)
        pygame.draw.rect(surface, (255, 100, 200), anim2_rect, width=3, border_radius=15)

        self._draw_decay_animation(surface, t, anim_box_x, anim2_box_y, anim1_box_w, anim2_box_h, active_w)

    def _get_text_height(self, text, max_w, font):
        words = text.split(" ")
        if not words: return 0
        lines_count = 1
        current_w = 0
        space_w = font.size(" ")[0]
        for word in words:
            word_w = font.size(word)[0]
            if current_w + word_w <= max_w:
                current_w += word_w + space_w
            else:
                lines_count += 1
                current_w = word_w + space_w
        return lines_count * font.get_linesize()

    def _draw_justified_text(self, surface, text, x, y, max_w, font):
        words = text.split(" ")
        if not words: return y
        lines, current_line, current_w = [], [], 0
        space_w = font.size(" ")[0]
        for word in words:
            word_w = font.size(word)[0]
            if current_w + word_w <= max_w:
                current_line.append(word)
                current_w += word_w + space_w
            else:
                lines.append(current_line)
                current_line = [word]
                current_w = word_w + space_w
        if current_line: lines.append(current_line)
        current_y = y
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            if not line: continue
            if i == len(lines) - 1 or len(line) == 1:
                cursor_x = x
                for word in line:
                    img = font.render(word, True, theme.WHITE)
                    surface.blit(img, (cursor_x, current_y))
                    cursor_x += img.get_width() + space_w
            else:
                total_words_w = sum(font.size(w)[0] for w in line)
                space_w_float = (max_w - total_words_w) / (len(line) - 1)
                cursor_x = float(x)
                for word in line:
                    img = font.render(word, True, theme.WHITE)
                    surface.blit(img, (int(cursor_x), current_y))
                    cursor_x += img.get_width() + space_w_float
            current_y += line_height
        return current_y

    def _draw_timer_animation(self, surface, t, cx, cy, active_w):
        # Partícula grande tremendo
        cycle = t % 2.0
        p_rad = int(active_w * 0.06)
        
        shake_x, shake_y = 0, 0
        if cycle < 1.5:
            # Aumenta a vibração conforme o tempo acaba
            intensidade = (cycle / 1.5) * 5
            shake_x = math.sin(t * 50) * intensidade
            shake_y = math.cos(t * 40) * intensidade
            
            # Pinta de uma cor quente
            pygame.draw.circle(surface, (250, 80, 80), (int(cx + shake_x), int(cy + shake_y)), p_rad)
            
            # Relogio (Cronômetro) rodando no centro
            angle = (cycle / 1.5) * 360
            end_x = cx + shake_x + (p_rad - 10) * math.sin(math.radians(angle))
            end_y = cy + shake_y - (p_rad - 10) * math.cos(math.radians(angle))
            pygame.draw.circle(surface, theme.WHITE, (int(cx + shake_x), int(cy + shake_y)), p_rad - 5, 2)
            pygame.draw.line(surface, theme.WHITE, (int(cx + shake_x), int(cy + shake_y)), (end_x, end_y), 4)
        else:
            # "POOF" Desapareceu
            f_lbl = theme.font(int(active_w * 0.04))
            lbl = f_lbl.render("Decaiu!", True, (255, 150, 200))
            surface.blit(lbl, lbl.get_rect(center=(cx, cy)))

        f_txt = theme.font(int(active_w * 0.025))
        lbl_bot = f_txt.render("Instabilidade", True, theme.WHITE)
        surface.blit(lbl_bot, lbl_bot.get_rect(midbottom=(cx, cy + p_rad + 20)))

    def _draw_decay_animation(self, surface, t, box_x, box_y, box_w, box_h, active_w):
        cycle = t % 2.5
        cx = box_x + box_w // 2
        cy = box_y + box_h // 2 + 10
        
        p_rad = int(active_w * 0.05)
        
        if cycle < 1.0:
            # Partícula mãe (Ex: Múon)
            pygame.draw.circle(surface, (180, 50, 200), (cx, cy), p_rad)
            f_sym = theme.font(int(p_rad * 1.5))
            lbl_sym = f_sym.render("μ", True, theme.WHITE)
            surface.blit(lbl_sym, lbl_sym.get_rect(center=(cx, cy)))
        else:
            # Ocorre a explosão e geram filhas
            progresso = (cycle - 1.0) / 1.5
            dist = int(active_w * 0.15 * progresso)
            
            # Elétron para a esquerda
            pygame.draw.circle(surface, (50, 150, 255), (cx - dist, cy + dist//2), p_rad//2)
            # Neutrino 1 pra cima
            pygame.draw.circle(surface, (100, 200, 150), (cx + dist//2, cy - dist), p_rad//3)
            # Neutrino 2 pra direita
            pygame.draw.circle(surface, (100, 200, 150), (cx + dist, cy + dist//2), p_rad//3)
            
            # Efeito de Flash central que some rápido
            if progresso < 0.2:
                s = pygame.Surface((p_rad * 4, p_rad * 4), pygame.SRCALPHA)
                alpha = int(255 * (1 - (progresso/0.2)))
                pygame.draw.circle(s, (255, 255, 255, alpha), (p_rad*2, p_rad*2), p_rad)
                surface.blit(s, (cx - p_rad*2, cy - p_rad*2))

        f_title = theme.font(int(active_w * 0.025))
        lbl = f_title.render("O Múon 'explode' em Elétron + Neutrinos", True, (255, 100, 200))
        surface.blit(lbl, lbl.get_rect(midtop=(cx, box_y + 15)))