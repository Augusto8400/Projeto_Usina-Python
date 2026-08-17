# -*- coding: utf-8 -*-
import math
import pygame
from screens.base import Screen
from ui import theme
from ui.widgets import draw_background, draw_title
from data.particles_data import FORCES

class ForcesScreen(Screen):
    def on_enter(self):
        super().on_enter()
        self.index = 0

    def handle_input(self, action):
        if action == "LEFT":
            self.index = (self.index - 1) % len(FORCES)
        elif action == "RIGHT":
            self.index = (self.index + 1) % len(FORCES)
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
        draw_title(surface, "FORÇAS FUNDAMENTAIS", center_x, title_y, size=int(active_w * 0.065))

        # 2. CONTROLES
        ctrl_y = title_y + int(self.height * 0.045)
        f_ctrl = theme.font(int(active_w * 0.028))
        
        joy_txt = f_ctrl.render("Mover", True, theme.WHITE)
        btn_b_txt = f_ctrl.render("Voltar", True, theme.WHITE)

        offset = int(active_w * 0.22)
        
        # JOYSTICK CRUZ
        joy_x = center_x - offset
        pygame.draw.rect(surface, theme.WHITE, (joy_x - 30, ctrl_y, 8, 20))
        pygame.draw.rect(surface, theme.WHITE, (joy_x - 36, ctrl_y + 6, 20, 8))
        
        # --- CORREÇÃO DE ESPAÇAMENTO ---
        # Empurrado ~15 pixels para a direita para fugir da cruz do joystick
        tri_y = ctrl_y + 10
        # Seta Esquerda
        pygame.draw.polygon(surface, theme.WHITE, [(joy_x - 5, tri_y), (joy_x + 1, tri_y - 6), (joy_x + 1, tri_y + 6)]) 
        
        # Texto "Mover"
        surface.blit(joy_txt, (joy_x + 6, ctrl_y - 2))
        
        # Seta Direita
        right_x = joy_x + 6 + joy_txt.get_width() + 6
        pygame.draw.polygon(surface, theme.WHITE, [(right_x + 6, tri_y), (right_x, tri_y - 6), (right_x, tri_y + 6)]) 
        
        # BOTÃO VERMELHO (Voltar)
        btn_b_x = center_x + offset
        pygame.draw.circle(surface, (220, 0, 0), (btn_b_x - 20, ctrl_y + 10), 12)
        pygame.draw.circle(surface, theme.WHITE, (btn_b_x - 20, ctrl_y + 10), 12, 2)
        surface.blit(btn_b_txt, (btn_b_x - 2, ctrl_y - 2))

        # 3. CAIXA DE TEXTO DIDÁTICO (SHRINK-WRAP)
        texto_box_y = ctrl_y + int(self.height * 0.035)
        texto_box_w = active_w - int(active_w * 0.16)
        texto_box_x = offset_x + int(active_w * 0.08)
        
        force = FORCES[self.index]
        nome_lower = force["name"].lower()
        
        if "forte" in nome_lower:
            texto_rico = "É a força mais poderosa da natureza! Ela atua como uma 'supercola' cósmica que une os Quarks para formar os Prótons e os Nêutrons.\n\nSem ela, o núcleo dos átomos explodiria instantaneamente devido à repulsão elétrica entre os prótons. Ela é mediada pelos Glúons e só funciona em distâncias minúsculas (dentro do núcleo atômico)."
        elif "eletromagn" in nome_lower or "elétrica" in nome_lower:
            texto_rico = "É a responsável por quase tudo que experimentamos no dia a dia: a luz, a eletricidade, o magnetismo, a química da vida e até a sensação de 'tocar' os objetos!\n\nEla faz com que partículas de cargas opostas se atraiam e iguais se repelem, mantendo os elétrons presos ao redor dos átomos. O seu mediador é o Fóton (a partícula da luz)."
        elif "fraca" in nome_lower:
            texto_rico = "Ao contrário das outras forças, esta não une nem empurra as coisas, mas sim as transforma. Ela é a responsável pela radioatividade e pela mudança de sabor dos quarks.\n\nÉ graças a essa força que ocorre a fusão nuclear que faz o Sol brilhar. Sem a Força Fraca, as estrelas não produziriam energia vital. Ela é mediada pelos pesados Bósons W e Z."
        else: # Gravidade
            texto_rico = "Curiosamente, é a força mais fraca de todas as quatro no mundo quântico das partículas, mas é a única com poder puramente acumulativo e de alcance infinito.\n\nÉ ela quem dita as regras do cosmos em grande escala: mantém os planetas em órbita, forma as galáxias e nos prende ao chão. Seu mediador teórico (Gráviton) ainda é um grande mistério."
        
        f_titulo_forca = theme.font(int(active_w * 0.055))
        f_mediador = theme.font(int(active_w * 0.03))
        f_texto = theme.font(int(active_w * 0.027))
        
        img_titulo = f_titulo_forca.render(force["name"].upper(), True, theme.GOLD)
        img_mediador = f_mediador.render(f"Mediador: {force['carrier']}", True, theme.CYAN)
        
        padding_topo = int(self.height * 0.025)
        altura_texto_total = padding_topo
        altura_texto_total += img_titulo.get_height() + int(self.height * 0.005)
        altura_texto_total += img_mediador.get_height() + int(self.height * 0.02)
        
        paragrafos = [p for p in texto_rico.split('\n') if p.strip()]
        
        for p in paragrafos:
            altura_texto_total += self._get_text_height(p, texto_box_w - 60, f_texto)
            altura_texto_total += int(self.height * 0.015) 
            
        altura_texto_total += int(self.height * 0.005)
        texto_box_h = altura_texto_total
        
        texto_rect = pygame.Rect(texto_box_x, texto_box_y, texto_box_w, texto_box_h)
        pygame.draw.rect(surface, (15, 20, 30), texto_rect, border_radius=15)
        pygame.draw.rect(surface, theme.GOLD, texto_rect, width=3, border_radius=15)
        
        cursor_y = texto_box_y + padding_topo
        surface.blit(img_titulo, img_titulo.get_rect(center=(center_x, cursor_y + img_titulo.get_height()//2)))
        cursor_y += img_titulo.get_height() + int(self.height * 0.005)
        
        surface.blit(img_mediador, img_mediador.get_rect(center=(center_x, cursor_y + img_mediador.get_height()//2)))
        cursor_y += img_mediador.get_height() + int(self.height * 0.02)
        
        for p in paragrafos:
            cursor_y = self._draw_justified_text(surface, p, texto_box_x + 30, cursor_y, texto_box_w - 60, f_texto)
            cursor_y += int(self.height * 0.015) 

        # 4. INDICADORES DO CARROSSEL
        dots_y = texto_box_y + texto_box_h + int(self.height * 0.015)
        total_forces = len(FORCES)
        dot_spacing = 25
        start_dot_x = center_x - ((total_forces - 1) * dot_spacing) // 2
        
        for i in range(total_forces):
            color = theme.GOLD if i == self.index else (80, 80, 100)
            radius = 6 if i == self.index else 4
            pygame.draw.circle(surface, color, (start_dot_x + i * dot_spacing, dots_y), radius)

        # 5. CAIXA DE ANIMAÇÃO (Alinhada com a base do Cubo da Home)
        anim_box_y = dots_y + int(self.height * 0.015)
        
        menu_y_home = int(self.height * 0.19)
        item_h_home = int(self.height * 0.045)
        cube_y_home = menu_y_home + (4 * item_h_home) + int(self.height * 0.05)
        cube_h_home = int(active_w * 0.8)
        base_home_y = cube_y_home + cube_h_home
        
        anim_box_h = base_home_y - anim_box_y
        if anim_box_h < int(self.height * 0.15):
            anim_box_h = int(self.height * 0.15)

        anim_rect = pygame.Rect(texto_box_x, anim_box_y, texto_box_w, anim_box_h)
        pygame.draw.rect(surface, (15, 20, 30), anim_rect, border_radius=15)
        
        surface.set_clip(anim_rect)
        self._draw_force_animation(surface, t, force["name"], center_x, anim_box_y + anim_box_h//2, active_w, texto_box_w)
        surface.set_clip(None)
        
        pygame.draw.rect(surface, theme.GOLD, anim_rect, width=3, border_radius=15)


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

    def _draw_force_animation(self, surface, t, name, cx, cy, active_w, box_w):
        n = name.lower()
        if "forte" in n:
            self._anim_strong(surface, t, cx, cy, active_w)
        elif "eletromagn" in n or "elétrica" in n:
            self._anim_em(surface, t, cx, cy, active_w, box_w)
        elif "fraca" in n:
            self._anim_weak(surface, t, cx, cy, active_w)
        else:
            self._anim_gravity(surface, t, cx, cy, active_w)

    def _anim_strong(self, surface, t, cx, cy, active_w):
        base_r = int(active_w * 0.08)
        r = base_r + math.sin(t * 8) * 10
        
        colors = [(255, 50, 50), (50, 255, 50), (50, 100, 255)] 
        points = []
        
        for i in range(3):
            angle = t + (i * 2 * math.pi / 3)
            qx = cx + math.cos(angle) * r
            qy = cy + math.sin(angle) * r
            points.append((qx, qy))
            
        pygame.draw.line(surface, theme.WHITE, points[0], points[1], 3)
        pygame.draw.line(surface, theme.WHITE, points[1], points[2], 3)
        pygame.draw.line(surface, theme.WHITE, points[2], points[0], 3)
        
        p_rad = int(active_w * 0.03)
        for i, (qx, qy) in enumerate(points):
            pygame.draw.circle(surface, colors[i], (int(qx), int(qy)), p_rad)
            pygame.draw.circle(surface, theme.WHITE, (int(qx), int(qy)), p_rad, 2)

    def _anim_em(self, surface, t, cx, cy, active_w, box_w):
        dist = int(active_w * 0.15) + math.sin(t * 4) * 15
        p_rad = int(active_w * 0.04)
        
        left_x = cx - dist
        right_x = cx + dist
        
        px = left_x + ((t * 250) % (dist * 2))
        py = cy + math.sin(px * 0.1) * 15 
        
        if left_x < px < right_x:
            pygame.draw.circle(surface, theme.GOLD, (int(px), int(py)), 6)
            
        pygame.draw.circle(surface, (255, 50, 50), (int(left_x), cy), p_rad)
        pygame.draw.circle(surface, (50, 150, 255), (int(right_x), cy), p_rad)
        
        f_sym = theme.font(int(p_rad * 1.5))
        lbl_pos = f_sym.render("+", True, theme.WHITE)
        lbl_neg = f_sym.render("-", True, theme.WHITE)
        
        surface.blit(lbl_pos, lbl_pos.get_rect(center=(int(left_x), cy - 2)))
        surface.blit(lbl_neg, lbl_neg.get_rect(center=(int(right_x), cy - 2)))

    def _anim_weak(self, surface, t, cx, cy, active_w):
        cycle = t % 4.0
        p_rad = int(active_w * 0.05)
        
        if cycle < 1.0:
            shake = math.sin(t * 40) * 4
            pygame.draw.circle(surface, (120, 120, 130), (int(cx + shake), cy), p_rad)
            f_lbl = theme.font(int(active_w * 0.025))
            lbl = f_lbl.render("Nêutron", True, theme.WHITE)
            surface.blit(lbl, lbl.get_rect(midtop=(int(cx + shake), cy + p_rad + 10)))
            
        elif cycle < 2.0:
            progresso = cycle - 1.0
            wx = cx + progresso * int(active_w * 0.2)
            
            pygame.draw.circle(surface, (255, 50, 50), (cx, cy), p_rad)
            pygame.draw.circle(surface, (150, 50, 200), (int(wx), cy), int(p_rad * 0.5))
            
            f_lbl = theme.font(int(active_w * 0.025))
            lbl_p = f_lbl.render("Próton", True, theme.WHITE)
            surface.blit(lbl_p, lbl_p.get_rect(midtop=(cx, cy + p_rad + 10)))
            
            lbl_w = f_lbl.render("W-", True, theme.WHITE)
            surface.blit(lbl_w, lbl_w.get_rect(midtop=(int(wx), cy + int(p_rad * 0.5) + 10)))
            
        else:
            progresso = cycle - 2.0
            wx = cx + int(active_w * 0.2)
            
            pygame.draw.circle(surface, (255, 50, 50), (cx, cy), p_rad)
            
            dist_x = progresso * int(active_w * 0.15)
            dist_y = progresso * int(active_w * 0.1)
            
            px_e = wx + dist_x
            py_e = cy - dist_y
            
            px_v = wx + dist_x
            py_v = cy + dist_y
            
            pygame.draw.circle(surface, (50, 150, 255), (int(px_e), int(py_e)), int(p_rad * 0.4))
            pygame.draw.circle(surface, (255, 255, 100), (int(px_v), int(py_v)), int(p_rad * 0.25))

    def _anim_gravity(self, surface, t, cx, cy, active_w):
        mass_rad = int(active_w * 0.06)
        orb_w = int(active_w * 0.18)
        orb_h = int(active_w * 0.05)
        
        pygame.draw.circle(surface, (200, 150, 80), (cx, cy), mass_rad)
        
        rect_orbita = pygame.Rect(cx - orb_w, cy - orb_h, orb_w * 2, orb_h * 2)
        pygame.draw.ellipse(surface, (100, 100, 100), rect_orbita, 2)
        
        ox = cx + math.cos(t * 2) * orb_w
        oy = cy + math.sin(t * 2) * orb_h
        
        is_behind = math.sin(t * 2) < 0
        color = (80, 100, 120) if is_behind else (150, 200, 255)
        
        pygame.draw.circle(surface, color, (int(ox), int(oy)), int(active_w * 0.02))