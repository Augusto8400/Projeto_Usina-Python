# -*- coding: utf-8 -*-
"""Widgets de desenho reutilizados por todas as telas."""
import random
import pygame

from ui import theme


class Starfield:
    """Fundo de estrelas piscando, gerado uma única vez (ao contrário
    do app React original, que recriava posições aleatórias a cada
    re-render — aqui geramos uma vez e reaproveitamos)."""

    def __init__(self, width, height, count=60):
        self.stars = [
            {
                "x": random.randint(0, width),
                "y": random.randint(0, height),
                "r": random.choice([1, 1, 2]),
                "phase": random.uniform(0, 6.28),
            }
            for _ in range(count)
        ]

    def draw(self, surface, t):
        for s in self.stars:
            brightness = 150 + int(105 * abs(pygame.math.Vector2(1, 0).rotate(
                (t * 60 + s["phase"] * 30) % 360).x))
            brightness = max(80, min(255, brightness))
            color = (brightness, brightness, 255)
            pygame.draw.circle(surface, color, (s["x"], s["y"]), s["r"])


def draw_background(surface, starfield, t):
    surface.fill(theme.BG_DARK)
    starfield.draw(surface, t)


def draw_title(surface, text, cx, y, size=48, color=theme.GOLD):
    f = theme.font(size)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        img = f.render(line, True, color)
        rect = img.get_rect(center=(cx, y + i * (size + 10)))
        # sombra retro
        shadow = f.render(line, True, (0, 0, 0))
        surface.blit(shadow, (rect.x + 3, rect.y + 3))
        surface.blit(img, rect)


def wrap_text(text, f, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        trial = (current + " " + w).strip()
        if f.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_paragraph(surface, text, x, y, max_width, size=22, color=theme.WHITE, line_gap=8):
    f = theme.font(size)
    lines = wrap_text(text, f, max_width)
    for i, line in enumerate(lines):
        img = f.render(line, True, color)
        surface.blit(img, (x, y + i * (size + line_gap)))
    return y + len(lines) * (size + line_gap)


def draw_panel(surface, rect, border_color=theme.PURPLE, bg=theme.PANEL_BG, width=3):
    pygame.draw.rect(surface, bg, rect)
    pygame.draw.rect(surface, border_color, rect, width)


def draw_menu_list(surface, items, selected_index, x, y, w, item_h=90, size=28):
    """Lista vertical de opções tipo menu de fliperama, navegável com
    CIMA/BAIXO. O item selecionado pisca em dourado com um cursor '>'."""
    f = theme.font(size)
    for i, label in enumerate(items):
        item_y = y + i * (item_h + 16)
        rect = pygame.Rect(x, item_y, w, item_h)
        is_sel = i == selected_index
        border = theme.GOLD if is_sel else theme.PURPLE
        draw_panel(surface, rect, border_color=border, width=4 if is_sel else 2)

        prefix = "> " if is_sel else "  "
        color = theme.GOLD if is_sel else theme.WHITE
        img = f.render(prefix + label, True, color)
        img_rect = img.get_rect(midleft=(rect.x + 24, rect.centery))
        surface.blit(img, img_rect)


def draw_footer_hint(surface, surf_w, surf_h, text, size=18):
    f = theme.font(size)
    img = f.render(text, True, theme.PURPLE)
    rect = img.get_rect(center=(surf_w // 2, surf_h - 30))
    surface.blit(img, rect)


def draw_table(surface, headers, rows, x, y, col_widths, size=18, row_h=42):
    f_head = theme.font(size)
    f_row = theme.font(size - 2)
    cx = x
    for h, cw in zip(headers, col_widths):
        img = f_head.render(h, True, theme.GOLD)
        surface.blit(img, (cx, y))
        cx += cw
    pygame.draw.line(surface, theme.PURPLE, (x, y + size + 6),
                      (x + sum(col_widths), y + size + 6), 2)

    ry = y + size + 16
    for row in rows:
        cx = x
        for cell, cw in zip(row, col_widths):
            color = cell[1] if isinstance(cell, tuple) else theme.WHITE
            text = cell[0] if isinstance(cell, tuple) else str(cell)
            img = f_row.render(text, True, color)
            surface.blit(img, (cx, ry))
            cx += cw
        ry += row_h
    return ry
