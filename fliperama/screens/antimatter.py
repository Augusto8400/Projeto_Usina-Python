# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title

class AntimatterScreen(Screen):
    def on_enter(self):
        super().on_enter()

    def handle_input(self, action):
        if action == "B":
            self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        
        # --- VIEWPORT RESPONSIVO ---
        is_landscape = self.width > self.height
        active_w = int(self.height * 0.5625) if is_landscape else self.width
        offset_x = (self.width - active_w) // 2
        center_x = offset_x + (active_w // 2)

        # 1. TÍTULO GERAL
        title_y = int(self.height * 0.04)
        draw_title(surface, "ANTIMATÉRIA", center_x, title_y, size=int(active_w * 0.08))

        # 2. CONTROLE "VOLTAR"
        ctrl_y = title_y + int(self.height * 0.045)
        f_ctrl = theme.font(int(active_w * 0.03))
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)
        
        total_w = 24 + 10 + btn_b_txt.get_width() 
        start_ctrl_x = center_x - (total_w // 2)
        
        pygame.draw.circle(surface, (220, 0, 0), (start_ctrl_x + 12, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (start_ctrl_x + 12, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (start_ctrl_x + 34, ctrl_y - 2))

        # 3. CÂMARA DE ANIMAÇÃO 
        anim_box_y = ctrl_y + int(self.height * 0.045)
        anim_box_h = int(self.height * 0.25)
        anim_box_w = active_w - int(active_w * 0.16)
        anim_box_x = offset_x + int(active_w * 0.08)

        anim_rect = pygame.Rect(anim_box_x, anim_box_y, anim_box_w, anim_box_h)
        pygame.draw.rect(surface, (15, 10, 25), anim_rect, border_radius=15)
        pygame.draw.rect(surface, theme.PURPLE, anim_rect, width=3, border_radius=15)

        self._draw_annihilation_animation(surface, t, center_x, anim_box_y + anim_box_h//2, active_w, anim_box_h)

        # 4. CAIXA DE TEXTO DIDÁTICO (SOB MEDIDA)
        texto_box_y = anim_box_y + anim_box_h + int(self.height * 0.02)
        
        paragrafos = [
            "Para cada partícula existe uma antipartícula com a mesma massa, mas com cargas opostas. O pósitron (antipartícula do elétron) foi a primeira a ser descoberta, em 1932, e hoje é usado em exames médicos (Tomografia PET).",
            "Quando uma partícula encontra sua antipartícula, ocorre a aniquilação: ambas desaparecem e se convertem em pura energia. O inverso também ocorre: energia extrema pode se converter em pares de matéria e antimatéria.",
            "Um dos maiores mistérios da física atual é o motivo pelo qual nosso Universo é dominado pela matéria. A antimatéria é extremamente rara, sendo produzida apenas na natureza em locais extremos, como buracos negros e tempestades de raios cósmicos."
        ]
        
        f_texto = theme.font(int(active_w * 0.031)) 
        
        # --- LÓGICA DO SHRINK-WRAP (CAIXA SOB MEDIDA) ---
        # Calcula exatamente qual será a altura ocupada por todo o texto antes de desenhar a caixa!
        padding_topo = int(self.height * 0.035)
        altura_texto_total = padding_topo
        
        for p in paragrafos:
            altura_texto_total += self._get_text_height(p, anim_box_w - 60, f_texto)
            altura_texto_total += int(self.height * 0.025) # Espaço entre parágrafos
            
        # O último espaço entre parágrafos já funciona como padding da base. Adiciona só um tiquinho pra simetria.
        altura_texto_total += int(self.height * 0.01)
        texto_box_h = altura_texto_total
        
        # Desenha o retângulo na altura perfeitamente calculada
        texto_rect = pygame.Rect(anim_box_x, texto_box_y, anim_box_w, texto_box_h)
        pygame.draw.rect(surface, (15, 10, 25), texto_rect, border_radius=15)
        pygame.draw.rect(surface, theme.PURPLE, texto_rect, width=3, border_radius=15)
        
        # Agora sim, desenha os textos por cima do retângulo
        cursor_y = texto_box_y + padding_topo 
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, anim_box_x + 30, cursor_y, anim_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.025) 

    # --- NOVA FUNÇÃO ---
    def _get_text_height(self, text, max_w, font):
        """Simula a quebra de linha para descobrir a altura total do parágrafo antes de desenhar"""
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
        """Função customizada para desenhar texto JUSTIFICADO no Pygame"""
        words = text.split(" ")
        if not words: return y
        
        lines = []
        current_line = []
        current_w = 0
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
        if current_line:
            lines.append(current_line)
            
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
                total_spaces_w = max_w - total_words_w
                space_w_float = total_spaces_w / (len(line) - 1)
                
                cursor_x = float(x)
                for word in line:
                    img = font.render(word, True, theme.WHITE)
                    surface.blit(img, (int(cursor_x), current_y))
                    cursor_x += img.get_width() + space_w_float
                    
            current_y += line_height
            
        return current_y


    def _draw_annihilation_animation(self, surface, t, cx, cy, active_w, box_h):
        cycle = t % 4.0
        p_radius = int(active_w * 0.045) 
        
        h_dist_max = int(active_w * 0.28) 
        v_dist_max = (box_h // 2) - p_radius - 15 
        
        f_lbl = theme.font(int(active_w * 0.022)) 
        
        if cycle < 1.8:
            progresso = cycle / 1.8
            ease = progresso ** 2 
            
            x_materia = cx - h_dist_max + int(h_dist_max * ease)
            x_antimateria = cx + h_dist_max - int(h_dist_max * ease)
            
            pygame.draw.circle(surface, (0, 150, 255), (x_materia, cy), p_radius)
            pygame.draw.circle(surface, theme.WHITE, (x_materia, cy), p_radius, 2)
            self._draw_superscript_symbol(surface, "e", "-", x_materia, cy, p_radius)
            lbl_m = f_lbl.render("Matéria", True, (150, 200, 255))
            surface.blit(lbl_m, lbl_m.get_rect(midtop=(x_materia, cy + p_radius + 8)))

            pygame.draw.circle(surface, (255, 50, 50), (x_antimateria, cy), p_radius)
            pygame.draw.circle(surface, theme.WHITE, (x_antimateria, cy), p_radius, 2)
            self._draw_superscript_symbol(surface, "e", "+", x_antimateria, cy, p_radius)
            lbl_a = f_lbl.render("Antimatéria", True, (255, 150, 150))
            surface.blit(lbl_a, lbl_a.get_rect(midtop=(x_antimateria, cy + p_radius + 8)))
            
        elif cycle < 2.2:
            progresso = (cycle - 1.8) / 0.4
            raio_explosao = int(p_radius * (1 + 2.5 * progresso))
            
            s = pygame.Surface((raio_explosao * 2, raio_explosao * 2), pygame.SRCALPHA)
            alpha = int(255 * (1 - progresso))
            
            pygame.draw.circle(s, (255, 255, 200, alpha), (raio_explosao, raio_explosao), raio_explosao)
            pygame.draw.circle(s, (255, 255, 255, alpha), (raio_explosao, raio_explosao), int(raio_explosao*0.6))
            surface.blit(s, (cx - raio_explosao, cy - raio_explosao))
            
        elif cycle < 3.8:
            progresso = (cycle - 2.2) / 1.6
            
            y_up = cy - int(v_dist_max * progresso)
            y_down = cy + int(v_dist_max * progresso)
            
            pygame.draw.circle(surface, theme.GOLD, (cx, y_up), p_radius)
            self._draw_superscript_symbol(surface, "γ", "", cx, y_up, p_radius, cor=(50, 50, 0))
            lbl_f1 = f_lbl.render("Energia (Fóton)", True, theme.GOLD)
            surface.blit(lbl_f1, lbl_f1.get_rect(midtop=(cx, y_up + p_radius + 5)))

            pygame.draw.circle(surface, theme.GOLD, (cx, y_down), p_radius)
            self._draw_superscript_symbol(surface, "γ", "", cx, y_down, p_radius, cor=(50, 50, 0))
            lbl_f2 = f_lbl.render("Energia (Fóton)", True, theme.GOLD)
            surface.blit(lbl_f2, lbl_f2.get_rect(midbottom=(cx, y_down - p_radius - 5)))


    def _draw_superscript_symbol(self, surface, base_text, super_text, cx, cy, radius, cor=theme.WHITE):
        f_base = theme.font(int(radius * 0.9))
        img_base = f_base.render(base_text, True, cor)
        
        if super_text:
            f_super = theme.font(int(radius * 0.5))
            img_super = f_super.render(super_text, True, cor)
            
            total_w = img_base.get_width() + img_super.get_width()
            start_x = cx - total_w // 2
            
            base_rect = img_base.get_rect(left=start_x, centery=cy)
            surface.blit(img_base, base_rect)
            
            super_rect = img_super.get_rect(left=base_rect.right, top=base_rect.top)
            surface.blit(img_super, super_rect)
        else:
            surface.blit(img_base, img_base.get_rect(center=(cx, cy)))