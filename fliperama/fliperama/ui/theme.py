# -*- coding: utf-8 -*-
"""Cores e fontes do tema retrô/espacial, portadas do CSS original."""
import os
import pygame

BG_DARK = (10, 5, 25)          # roxo bem escuro do fundo
PANEL_BG = (26, 11, 46)        # #1a0b2e
PURPLE = (123, 104, 238)       # #7b68ee — bordas
GOLD = (255, 215, 0)           # #ffd700 — destaques / título
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (240, 240, 255)
RED = (255, 80, 80)
GREEN = (100, 255, 140)

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts")


def _find_pixel_font():
    """Procura por uma fonte pixelada em assets/fonts/. Se não achar,
    usa uma fonte monoespaçada do sistema como alternativa (ainda dá
    um ar retrô, só não é pixel-perfect)."""
    if os.path.isdir(FONT_DIR):
        for fname in os.listdir(FONT_DIR):
            if fname.lower().endswith((".ttf", ".otf")):
                return os.path.join(FONT_DIR, fname)
    return None


_PIXEL_FONT_PATH = None  # resolvido em init_fonts()
_FONT_CACHE = {}


def init_fonts():
    global _PIXEL_FONT_PATH
    _PIXEL_FONT_PATH = _find_pixel_font()
    if _PIXEL_FONT_PATH:
        print(f"[ui] usando fonte pixelada: {_PIXEL_FONT_PATH}")
    else:
        print("[ui] nenhuma fonte .ttf/.otf em assets/fonts/ — usando "
              "monoespaçada do sistema. Para o visual 8-bit completo, "
              "baixe uma fonte tipo 'Press Start 2P' e coloque nessa pasta.")


def font(size):
    if size not in _FONT_CACHE:
        if _PIXEL_FONT_PATH:
            _FONT_CACHE[size] = pygame.font.Font(_PIXEL_FONT_PATH, size)
        else:
            _FONT_CACHE[size] = pygame.font.SysFont("couriernew,monospace", size, bold=True)
    return _FONT_CACHE[size]
