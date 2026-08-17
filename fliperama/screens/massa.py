# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title

class MassaScreen(Screen):
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
        draw_title(surface, "MASSA", center_x, title_y, size=int(active_w * 0.08))

        ctrl_y = title_y + int(self.height * 0.04)
        f_ctrl = theme.font(int(active_w * 0.03))
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)
        
        total_w = 24 + 10 + btn_b_txt.get_width() 
        start_ctrl_x = center_x - (total_w // 2)
        
        pygame.draw.circle(surface, (220, 0, 0), (start_ctrl_x + 12, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (start_ctrl_x + 12, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (start_ctrl_x + 34, ctrl_y - 2))

        # ANIMAÇÃO SUPERIOR (Campo de Higgs)
        anim1_box_y = ctrl_y + int(self.height * 0.035)
        anim1_box_h = int(self.height * 0.14) 
        anim1_box_w = active_w - int(active_w * 0.16)
        anim_box_x = offset_x + int(active_w * 0.08)

        anim1_rect = pygame.Rect(anim_box_x, anim1_box_y, anim1_box_w, anim1_box_h)
        
        # Desenha o fundo da caixa primeiro
        pygame.draw.rect(surface, (15, 20, 30), anim1_rect, border_radius=15)

        # --- MÁSCARA DE CORTE (CLIP) ---
        # Restringe o desenho APENAS para a área de dentro da caixa!
        surface.set_clip(anim1_rect)
        self._draw_higgs_animation(surface, t, center_x, anim1_box_y + anim1_box_h//2, active_w, anim1_box_w)
        surface.set_clip(None) # Libera a máscara da tela inteira
        
        # Desenha a borda Dourada POR CIMA da animação para um acabamento liso nas quinas
        pygame.draw.rect(surface, (255, 180, 50), anim1_rect, width=3, border_radius=15)

        # TEXTO DIDÁTICO
        texto_box_y = anim1_box_y + anim1_box_h + int(self.height * 0.015)
        
        paragrafos = [
            "A massa é o que conhecemos popularmente como o 'peso' das coisas. No mundo microscópico, as partículas não têm massa por conta própria. Elas ganham massa porque precisam nadar através de um 'melaço' invisível que preenche todo o universo, chamado de Campo de Higgs.",
            "Partículas leves, como o Elétron, interagem muito pouco com esse melaço, então conseguem se mover rapidamente. O Fóton (a luz) não interage nada com ele, por isso não tem massa e viaja na maior velocidade possível!",
            "Já o Quark Top interage intensamente com esse campo, sendo puxado e arrastado. Isso faz com que ele seja a partícula mais pesada já descoberta na natureza, tendo o peso equivalente a um átomo inteiro de ouro."
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
        pygame.draw.rect(surface, (255, 180, 50), texto_rect, width=3, border_radius=15)
        
        cursor_y = texto_box_y + padding_topo 
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, anim_box_x + 30, cursor_y, anim1_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.015) 

        # ANIMAÇÃO INFERIOR (Balança / Diferença de Massas) sincronizada com a Home
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
        pygame.draw.rect(surface, (255, 180, 50), anim2_rect, width=3, border_radius=15)

        self._draw_scale_animation(surface, t, anim_box_x, anim2_box_y, anim1_box_w, anim2_box_h, active_w)

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

    def _draw_higgs_animation(self, surface, t, cx, cy, active_w, box_w):
        offset_dots = (t * 20) % 40
        for i in range(-20, box_w + 40, 40):
            for j in range(-40, 40, 20):
                pygame.draw.circle(surface, (80, 60, 20), (int(cx - box_w/2 + i - offset_dots), cy + j), 2)
        
        x_foton = cx - box_w//2 + ((t * 250) % (box_w + 40)) - 20
        pygame.draw.circle(surface, theme.GOLD, (int(x_foton), cy - 20), 8)
        
        x_top = cx - box_w//2 + ((t * 40) % (box_w + 100)) - 50
        radius_top = int(active_w * 0.05)
        
        # Aura de interação (Usando Surface pra garantir a transparência verdadeira do Pygame)
        s = pygame.Surface((radius_top*2 + 20, radius_top*2 + 20), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 180, 50, 100), (radius_top + 10, radius_top + 10), radius_top + 10)
        surface.blit(s, (int(x_top) - radius_top - 10, cy + 15 - radius_top - 10))
        
        pygame.draw.circle(surface, (200, 50, 50), (int(x_top), cy + 15), radius_top)
        
        f_lbl = theme.font(int(active_w * 0.022))
        lbl_f = f_lbl.render("S/ Massa", True, theme.GOLD)
        surface.blit(lbl_f, lbl_f.get_rect(midbottom=(int(x_foton), cy - 35)))
        
        lbl_t = f_lbl.render("Pesado", True, (255, 180, 50))
        surface.blit(lbl_t, lbl_t.get_rect(midtop=(int(x_top), cy + 15 + radius_top + 5)))

    def _draw_scale_animation(self, surface, t, box_x, box_y, box_w, box_h, active_w):
        cx = box_x + box_w // 2
        cy = box_y + box_h // 2 + 10
        
        angle = math.sin(t * 2) * 10 - 15  
        
        arm_len = int(active_w * 0.15)
        left_x = cx - arm_len * math.cos(math.radians(angle))
        left_y = cy - arm_len * math.sin(math.radians(angle))
        right_x = cx + arm_len * math.cos(math.radians(angle))
        right_y = cy + arm_len * math.sin(math.radians(angle))
        
        pygame.draw.polygon(surface, (150, 150, 150), [(cx, cy), (cx-15, cy+40), (cx+15, cy+40)])
        pygame.draw.line(surface, theme.WHITE, (left_x, left_y), (right_x, right_y), 4)
        
        top_rad = int(active_w * 0.05)
        pygame.draw.circle(surface, (200, 50, 50), (int(left_x), int(left_y - top_rad)), top_rad)
        f_lbl = theme.font(int(active_w * 0.02))
        lbl_t = f_lbl.render("Quark Top", True, theme.WHITE)
        surface.blit(lbl_t, lbl_t.get_rect(midbottom=(int(left_x), int(left_y - top_rad*2 - 5))))
        
        ele_rad = int(active_w * 0.015)
        pygame.draw.circle(surface, (50, 150, 255), (int(right_x), int(right_y - ele_rad)), ele_rad)
        lbl_e = f_lbl.render("Elétron", True, theme.WHITE)
        surface.blit(lbl_e, lbl_e.get_rect(midbottom=(int(right_x), int(right_y - ele_rad*2 - 5))))