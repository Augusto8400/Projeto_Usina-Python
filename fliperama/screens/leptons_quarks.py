# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title
from data.particles_data import LEPTONS, QUARKS

class LeptonsQuarksScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.index = 0 # 0 = Quarks, 1 = Léptons

    def handle_input(self, action):
        if action == "LEFT":
            self.index = (self.index - 1) % 2
        elif action == "RIGHT":
            self.index = (self.index + 1) % 2
        elif action == "B":
            self.next_screen = "home"

    def draw(self, surface, t):
        draw_background(surface, self.starfield, t)
        
        # --- VIEWPORT RESPONSIVO ---
        is_landscape = self.width > self.height
        active_w = int(self.height * 0.5625) if is_landscape else self.width
        offset_x = (self.width - active_w) // 2
        center_x = offset_x + (active_w // 2)

        # 1. TÍTULO GERAL
        title_y = int(self.height * 0.035)
        draw_title(surface, "LÉPTONS E QUARKS", center_x, title_y, size=int(active_w * 0.065))

        # 2. CONTROLES (Carrossel)
        ctrl_y = title_y + int(self.height * 0.045)
        f_ctrl = theme.font(int(active_w * 0.028))
        
        joy_txt = f_ctrl.render("Mover", True, theme.WHITE)
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)

        offset = int(active_w * 0.22)
        
        joy_x = center_x - offset
        pygame.draw.rect(surface, theme.WHITE, (joy_x - 30, ctrl_y, 8, 20))
        pygame.draw.rect(surface, theme.WHITE, (joy_x - 36, ctrl_y + 6, 20, 8))
        
        tri_y = ctrl_y + 10
        pygame.draw.polygon(surface, theme.WHITE, [(joy_x - 5, tri_y), (joy_x + 1, tri_y - 6), (joy_x + 1, tri_y + 6)]) 
        surface.blit(joy_txt, (joy_x + 6, ctrl_y - 2))
        right_x = joy_x + 6 + joy_txt.get_width() + 6
        pygame.draw.polygon(surface, theme.WHITE, [(right_x + 6, tri_y), (right_x, tri_y - 6), (right_x, tri_y + 6)]) 
        
        btn_b_x = center_x + offset
        pygame.draw.circle(surface, (220, 0, 0), (btn_b_x - 20, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (btn_b_x - 20, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (btn_b_x - 2, ctrl_y - 2))

        # 3. LÓGICA DO CARROSSEL
        if self.index == 0:
            title = "Quarks"
            subtitle = "Blocos de construção da matéria"
            particles = QUARKS
            c_border = (255, 60, 110)
            c_bg = (40, 10, 20)
            texto_rico = "Os Quarks são os blocos fundamentais que formam a matéria que podemos tocar. Eles são extremamente 'sociais' e nunca andam sozinhos na natureza, estando sempre presos uns aos outros por uma força superpoderosa (Força Forte).\n\nExistem 6 tipos. Os quarks Up e Down são os mais comuns, formando os Prótons e Nêutrons dos átomos. Os outros quatro são muito pesados e instáveis, existindo apenas por frações de segundo no universo."
        else:
            title = "Léptons"
            subtitle = "Família do elétron e neutrinos"
            particles = LEPTONS
            c_border = (0, 200, 255)
            c_bg = (10, 30, 40)
            texto_rico = "Os Léptons são partículas independentes e solitárias. Ao contrário dos quarks, eles ignoram completamente a 'supercola' da Força Forte e preferem voar livremente pelo espaço.\n\nO membro mais famoso dessa família é o Elétron, o criador da eletricidade. A família também inclui os Neutrinos: partículas 'fantasmas' minúsculas e neutras que viajam perto da velocidade da luz e atravessam planetas inteiros sem bater em nada!"

        # 4. DESENHA A GRADE (3x2)
        grid_start_y = ctrl_y + int(self.height * 0.04)
        grid_bottom = self._draw_particle_group(surface, title, subtitle, particles, c_border, c_bg, grid_start_y, offset_x, active_w)

        # 5. CAIXA DE TEXTO DIDÁTICO (SHRINK-WRAP)
        texto_box_y = grid_bottom + int(self.height * 0.015)
        texto_box_w = active_w - int(active_w * 0.16)
        texto_box_x = offset_x + int(active_w * 0.08)
        
        f_texto = theme.font(int(active_w * 0.026))
        
        padding_topo = int(self.height * 0.02)
        altura_texto_total = padding_topo
        
        paragrafos = [p for p in texto_rico.split('\n') if p.strip()]
        for p in paragrafos:
            altura_texto_total += self._get_text_height(p, texto_box_w - 60, f_texto)
            altura_texto_total += int(self.height * 0.015) 
            
        altura_texto_total += int(self.height * 0.005)
        texto_box_h = altura_texto_total
        
        texto_rect = pygame.Rect(texto_box_x, texto_box_y, texto_box_w, texto_box_h)
        pygame.draw.rect(surface, (15, 20, 30), texto_rect, border_radius=15)
        pygame.draw.rect(surface, c_border, texto_rect, width=3, border_radius=15)
        
        cursor_y = texto_box_y + padding_topo
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, texto_box_x + 30, cursor_y, texto_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.015) 

        # 6. INDICADORES DO CARROSSEL
        dots_y = texto_box_y + texto_box_h + int(self.height * 0.015)
        dot_spacing = 25
        start_dot_x = center_x - dot_spacing // 2
        
        for i in range(2):
            color = theme.GOLD if i == self.index else (80, 80, 100)
            radius = 6 if i == self.index else 4
            pygame.draw.circle(surface, color, (start_dot_x + i * dot_spacing, dots_y), radius)

        # 7. CAIXA DE ANIMAÇÃO (Altura limite aumentada para evitar corte do texto)
        anim_box_y = dots_y + int(self.height * 0.015)
        
        menu_y_home = int(self.height * 0.19)
        item_h_home = int(self.height * 0.045)
        cube_y_home = menu_y_home + (4 * item_h_home) + int(self.height * 0.05)
        cube_h_home = int(active_w * 0.8)
        base_home_y = cube_y_home + cube_h_home
        
        anim_box_h = base_home_y - anim_box_y
        
        # O limite mínimo aumentou de 12% para 16% para dar respiro ao texto inferior!
        if anim_box_h < int(self.height * 0.16):
            anim_box_h = int(self.height * 0.16)

        anim_rect = pygame.Rect(texto_box_x, anim_box_y, texto_box_w, anim_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim_rect, border_radius=15)
        
        surface.set_clip(anim_rect)
        if self.index == 0:
            self._draw_quarks_animation(surface, t, center_x, anim_box_y + anim_box_h//2, active_w)
        else:
            self._draw_leptons_animation(surface, t, center_x, anim_box_y + anim_box_h//2, active_w, texto_box_w)
        surface.set_clip(None)
        
        pygame.draw.rect(surface, c_border, anim_rect, width=3, border_radius=15)


    def _draw_particle_group(self, surface, title, subtitle, particles, color_border, color_bg, start_y, offset_x, active_w):
        margin_x = offset_x + int(active_w * 0.08)
        
        f_title = theme.font(int(active_w * 0.055))
        f_sub = theme.font(int(active_w * 0.028)) 
        
        lbl_title = f_title.render(title, True, color_border)
        lbl_sub = f_sub.render(subtitle, True, (150, 150, 150))
        
        surface.blit(lbl_title, (margin_x, start_y))
        surface.blit(lbl_sub, (margin_x + lbl_title.get_width() + 15, start_y + int(active_w * 0.025)))
        
        grid_start_y = start_y + int(self.height * 0.045)
        grid_w = active_w - int(active_w * 0.16)
        card_w = (grid_w - 40) // 3 
        card_h = int(card_w * 0.88) 
        gap_y = int(self.height * 0.015) 
        
        col_counts = [0, 0, 0] 
        
        for p in particles:
            try:
                gen_val = int(str(p.get("generation", 1))[0])
            except ValueError:
                gen_val = 1
                
            col = gen_val - 1 
            if col < 0 or col > 2:
                col = 0
                
            row = col_counts[col]
            if row > 1:
                row = 1
                
            col_counts[col] += 1
            
            x = margin_x + col * (card_w + 20)
            y = grid_start_y + row * (card_h + gap_y)
            card_rect = pygame.Rect(x, y, card_w, card_h)
            
            pygame.draw.rect(surface, color_bg, card_rect, border_radius=15)
            pygame.draw.rect(surface, color_border, card_rect, width=3, border_radius=15)
            
            f_small = theme.font(int(card_w * 0.13))
            gen_img = f_small.render(f"G{col + 1}", True, (150, 150, 150))
            charge_img = f_small.render(str(p.get("charge", "")), True, color_border)
            
            surface.blit(gen_img, (x + 10, y + 8))
            surface.blit(charge_img, (x + card_w - charge_img.get_width() - 10, y + 8))
            
            raw_name = p.get("name", "")
            clean_name = raw_name.split("(")[0].strip()
            
            if "neutrino" in clean_name.lower() and " " in clean_name:
                partes = clean_name.split(" ", 1)
                linhas_nome = [partes[0].capitalize(), partes[1].title()]
            else:
                linhas_nome = [clean_name.capitalize()]
            
            f_name = theme.font(int(card_w * 0.115))
            y_offset = card_h - 10
            for linha in reversed(linhas_nome):
                name_img = f_name.render(linha, True, theme.WHITE)
                surface.blit(name_img, name_img.get_rect(midbottom=(x + card_w//2, y + y_offset)))
                y_offset -= name_img.get_height() + 2
            
            safe_symbols = {
                "Elétron": ("e", ""), "Múon": ("μ", ""), "Tau": ("τ", ""),
                "Neutrino do elétron": ("ν", "e"), "Neutrino do múon": ("ν", "μ"), "Neutrino do tau": ("ν", "τ"),
                "Up": ("u", ""), "Down": ("d", ""), "Charm": ("c", ""), "Strange": ("s", ""), "Top": ("t", ""), "Bottom": ("b", ""),
                "Quark up": ("u", ""), "Quark down": ("d", ""), "Quark charm": ("c", ""), "Quark strange": ("s", ""), "Quark top": ("t", ""), "Quark bottom": ("b", "")
            }
            base_char, sub_char = safe_symbols.get(clean_name.capitalize(), (clean_name[0] if clean_name else "?", ""))
            
            f_sym = theme.font(int(card_h * 0.45))
            sym_img = f_sym.render(base_char, True, color_border)
            sym_y = y + card_h//2 - (8 if len(linhas_nome) > 1 else 0)

            if sub_char:
                f_sub = theme.font(int(card_h * 0.25))
                sub_img = f_sub.render(sub_char, True, color_border)
                total_w = sym_img.get_width() + sub_img.get_width()
                start_x = x + card_w//2 - total_w//2
                
                base_rect = sym_img.get_rect(left=start_x, centery=sym_y)
                surface.blit(sym_img, base_rect)
                sub_rect = sub_img.get_rect(left=base_rect.right, bottom=base_rect.bottom - 4)
                surface.blit(sub_img, sub_rect)
            else:
                surface.blit(sym_img, sym_img.get_rect(center=(x + card_w//2, sym_y)))

        return grid_start_y + 2 * (card_h + gap_y)

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

    def _draw_quarks_animation(self, surface, t, cx, cy, active_w):
        # Reduzido de 0.08 para 0.07 para a partícula inteira subir um pouco
        p_rad = int(active_w * 0.07)
        
        pygame.draw.circle(surface, (50, 20, 30), (cx, cy), p_rad + 15)
        pygame.draw.circle(surface, (255, 60, 110), (cx, cy), p_rad + 15, 2)
        
        vib = math.sin(t * 10) * 3
        
        q_rad = int(active_w * 0.025)
        pos = [
            (cx - p_rad//2 + vib, cy - p_rad//3 - vib), 
            (cx + p_rad//2 - vib, cy - p_rad//3 + vib), 
            (cx, cy + p_rad//2 + vib)                   
        ]
        labels = ["u", "u", "d"]
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)] 
        
        pygame.draw.line(surface, theme.WHITE, pos[0], pos[1], 2)
        pygame.draw.line(surface, theme.WHITE, pos[1], pos[2], 2)
        pygame.draw.line(surface, theme.WHITE, pos[2], pos[0], 2)
        
        f_lbl = theme.font(int(q_rad * 1.5))
        for i, (x, y) in enumerate(pos):
            pygame.draw.circle(surface, colors[i], (int(x), int(y)), q_rad)
            pygame.draw.circle(surface, theme.WHITE, (int(x), int(y)), q_rad, 1)
            img = f_lbl.render(labels[i], True, theme.WHITE)
            surface.blit(img, img.get_rect(center=(int(x), int(y))))
            
        f_title = theme.font(int(active_w * 0.025))
        lbl = f_title.render("Confinamento dentro de um Próton", True, (255, 150, 180))
        # O texto subiu para +15 em vez de +25
        surface.blit(lbl, lbl.get_rect(midtop=(cx, cy + p_rad + 15)))

    def _draw_leptons_animation(self, surface, t, cx, cy, active_w, box_w):
        nuc_rad = int(active_w * 0.03)
        orb_w = int(active_w * 0.15)
        orb_h = int(active_w * 0.05)
        
        pygame.draw.circle(surface, (200, 50, 50), (cx, cy), nuc_rad)
        pygame.draw.ellipse(surface, (100, 150, 200), pygame.Rect(cx - orb_w, cy - orb_h, orb_w*2, orb_h*2), 1)
        
        e_x = cx + math.cos(t * 3) * orb_w
        e_y = cy + math.sin(t * 3) * orb_h
        pygame.draw.circle(surface, (0, 200, 255), (int(e_x), int(e_y)), int(active_w * 0.015))
        
        f_simb = theme.font(int(active_w * 0.02))
        lbl_e = f_simb.render("e-", True, theme.WHITE)
        surface.blit(lbl_e, lbl_e.get_rect(midbottom=(int(e_x), int(e_y) - 5)))
        
        v_x = cx - box_w//2 + ((t * 400) % (box_w + 100)) - 50
        v_y = cy + 20
        pygame.draw.circle(surface, (150, 255, 200), (int(v_x), v_y), int(active_w * 0.01))
        
        pygame.draw.line(surface, (150, 255, 200), (int(v_x)-20, v_y), (int(v_x), v_y), 2)
        
        lbl_v = f_simb.render("ν", True, theme.WHITE)
        surface.blit(lbl_v, lbl_v.get_rect(midbottom=(int(v_x), v_y - 5)))

        f_title = theme.font(int(active_w * 0.025))
        lbl = f_title.render("O Neutrino atravessa a matéria como um fantasma!", True, (150, 255, 200))
        # O texto subiu para +12 em vez de +20
        surface.blit(lbl, lbl.get_rect(midtop=(cx, cy + orb_h + 12)))