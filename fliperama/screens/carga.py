# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title

class CargaScreen(Screen):
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
        draw_title(surface, "CARGA", center_x, title_y, size=int(active_w * 0.08))

        ctrl_y = title_y + int(self.height * 0.04)
        f_ctrl = theme.font(int(active_w * 0.03))
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)
        
        total_w = 24 + 10 + btn_b_txt.get_width() 
        start_ctrl_x = center_x - (total_w // 2)
        
        pygame.draw.circle(surface, (220, 0, 0), (start_ctrl_x + 12, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (start_ctrl_x + 12, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (start_ctrl_x + 34, ctrl_y - 2))

        # ANIMAÇÃO SUPERIOR (Atração Eletromagnética)
        anim1_box_y = ctrl_y + int(self.height * 0.035)
        anim1_box_h = int(self.height * 0.14) 
        anim1_box_w = active_w - int(active_w * 0.16)
        anim_box_x = offset_x + int(active_w * 0.08)

        anim1_rect = pygame.Rect(anim_box_x, anim1_box_y, anim1_box_w, anim1_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim1_rect, border_radius=15)
        pygame.draw.rect(surface, (100, 255, 150), anim1_rect, width=3, border_radius=15)

        self._draw_attraction_animation(surface, t, center_x, anim1_box_y + anim1_box_h//2, active_w)

        # TEXTO DIDÁTICO
        texto_box_y = anim1_box_y + anim1_box_h + int(self.height * 0.015)
        
        paragrafos = [
            "Você já brincou com ímãs e notou que eles podem se atrair com força ou se repelir intensamente dependendo do lado? A Carga Elétrica das partículas funciona exatamente com essa mesma regra mágica da natureza.",
            "Partículas com cargas opostas (positivo e negativo) se apaixonam e se atraem. É essa força de atração que mantém os elétrons (negativos) girando ao redor do núcleo do átomo (positivo), permitindo que a química e a vida existam.",
            "Por outro lado, partículas com a mesma carga (duas negativas ou duas positivas) sentem uma aversão extrema e se repelem ativamente. Se uma partícula não tem carga nenhuma, como o Neutrino, ela vira um 'fantasma' magnético, passando reto sem sentir atração nem repulsão."
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
        pygame.draw.rect(surface, (100, 255, 150), texto_rect, width=3, border_radius=15)
        
        cursor_y = texto_box_y + padding_topo 
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, anim_box_x + 30, cursor_y, anim1_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.015) 

        # ANIMAÇÃO INFERIOR (Repulsão)
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
        pygame.draw.rect(surface, (100, 255, 150), anim2_rect, width=3, border_radius=15)

        self._draw_repulsion_animation(surface, t, anim_box_x, anim2_box_y, anim1_box_w, anim2_box_h, active_w)

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

    def _draw_attraction_animation(self, surface, t, cx, cy, active_w):
        cycle = t % 2.0
        p_rad = int(active_w * 0.04)
        dist_max = int(active_w * 0.25)
        
        f_simbol = theme.font(int(active_w * 0.05))
        
        if cycle < 1.0:
            progresso = cycle / 1.0
            ease = progresso ** 1.5 
            offset = dist_max - int(dist_max * ease)
            
            # Atrito de partículas opostas (Opostos se atraem)
            pygame.draw.circle(surface, (255, 50, 50), (cx - offset, cy), p_rad) # Positivo
            pygame.draw.circle(surface, (50, 150, 255), (cx + offset, cy), p_rad) # Negativo
            
            lbl_pos = f_simbol.render("+", True, theme.WHITE)
            surface.blit(lbl_pos, lbl_pos.get_rect(center=(cx - offset, cy - 2)))
            
            lbl_neg = f_simbol.render("-", True, theme.WHITE)
            surface.blit(lbl_neg, lbl_neg.get_rect(center=(cx + offset, cy - 2)))
        else:
            # Colisão
            pygame.draw.circle(surface, (200, 100, 150), (cx, cy), p_rad)
            s = pygame.Surface((p_rad*4, p_rad*4), pygame.SRCALPHA)
            alpha = int(255 * (1 - (cycle-1.0)))
            pygame.draw.circle(s, (255, 255, 255, alpha), (p_rad*2, p_rad*2), int(p_rad*1.5), 4)
            surface.blit(s, (cx - p_rad*2, cy - p_rad*2))
            
        f_lbl = theme.font(int(active_w * 0.025))
        lbl = f_lbl.render("Opostos se Atraem", True, (100, 255, 150))
        surface.blit(lbl, lbl.get_rect(midbottom=(cx, cy - p_rad - 15)))

    def _draw_repulsion_animation(self, surface, t, box_x, box_y, box_w, box_h, active_w):
        cycle = t % 2.0
        cx = box_x + box_w // 2
        cy = box_y + box_h // 2 + 10
        p_rad = int(active_w * 0.04)
        dist_max = int(active_w * 0.2)
        
        f_simbol = theme.font(int(active_w * 0.05))
        
        # Iguaus se repelem (Ambas negativas)
        progresso = cycle / 2.0
        ease = 1 - (1 - progresso) ** 3 # Desacelera ao afastar
        
        offset = p_rad + int(dist_max * ease)
        
        pygame.draw.circle(surface, (50, 150, 255), (cx - offset, cy), p_rad) 
        pygame.draw.circle(surface, (50, 150, 255), (cx + offset, cy), p_rad)
        
        lbl_neg1 = f_simbol.render("-", True, theme.WHITE)
        surface.blit(lbl_neg1, lbl_neg1.get_rect(center=(cx - offset, cy - 2)))
        
        lbl_neg2 = f_simbol.render("-", True, theme.WHITE)
        surface.blit(lbl_neg2, lbl_neg2.get_rect(center=(cx + offset, cy - 2)))
        
        # Setas empurrando para fora
        if offset > p_rad + 10:
            pygame.draw.line(surface, theme.WHITE, (cx - offset - p_rad - 5, cy), (cx - offset - p_rad - 25, cy), 3)
            pygame.draw.line(surface, theme.WHITE, (cx + offset + p_rad + 5, cy), (cx + offset + p_rad + 25, cy), 3)

        f_lbl = theme.font(int(active_w * 0.025))
        lbl = f_lbl.render("Iguais se Repelem", True, (100, 255, 150))
        surface.blit(lbl, lbl.get_rect(midtop=(cx, box_y + 15)))