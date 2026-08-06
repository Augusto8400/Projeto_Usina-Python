# -*- coding: utf-8 -*-
"""
Fliperama de Partículas Elementares — ponto de entrada.

Roda em Raspberry Pi com:
  - TV vertical (portrait) como tela
  - Botões CIMA/BAIXO/ESQ/DIR + A/B ligados ao GPIO
  - Leitor RFID MFRC522, lendo cubos com tags coladas

Para testar no PC sem hardware nenhum, basta rodar:
    python3 main.py
O programa detecta a ausência de gpiozero/mfrc522 e usa automaticamente
o teclado (setas + ENTER/ESC) e as teclas 1-8 para simular os cubos.
"""
import sys
import time

import pygame

import config
from ui import theme
from hardware.input_handler import InputHandler
from hardware.rfid_reader import RFIDReader
from data.particles_data import PARTICLES
from data.rfid_map import RFID_MAP  # gerado a partir de rfid_map.json

from screens.home import HomeScreen
from screens.cube_reader import CubeReaderScreen
from screens.leptons_quarks import LeptonsQuarksScreen
from screens.antimatter import AntimatterScreen
from screens.hadron_game import HadronGameScreen
from screens.forces import ForcesScreen
from screens.spin import SpinScreen
from screens.quiz import QuizScreen

SCREEN_CLASSES = {
    "home": HomeScreen,
    "cube_reader": CubeReaderScreen,
    "leptons_quarks": LeptonsQuarksScreen,
    "antimatter": AntimatterScreen,
    "hadron_game": HadronGameScreen,
    "forces": ForcesScreen,
    "spin": SpinScreen,
    "quiz": QuizScreen,
}

# teclas 1-8 simulam os cubos, em modo desenvolvimento sem RFID real
MOCK_CUBE_KEYS = {
    pygame.K_1: "eletron",
    pygame.K_2: "quark_up",
    pygame.K_3: "quark_down",
    pygame.K_4: "foton",
    pygame.K_5: "neutrino",
    pygame.K_6: "gluon",
    pygame.K_7: "positron",
    pygame.K_8: "higgs",
}


class App:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        if config.FULLSCREEN:
            info = pygame.display.Info()
            self.width, self.height = info.current_w, info.current_h
            self.surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.width, self.height = config.WINDOW_SIZE
            self.surface = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Partículas Elementares — Fliperama")
        theme.init_fonts()

        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.running = True

        self.input = InputHandler()

        # instancia todas as telas uma vez (mantém estado ao trocar de tela
        # seria possível, mas aqui recriamos o estado sempre via on_enter)
        self.screens = {name: cls(self) for name, cls in SCREEN_CLASSES.items()}
        self.current_name = "home"
        self.current = self.screens[self.current_name]
        self.current.on_enter()

        self.rfid = RFIDReader(self._on_rfid_placed, self._on_rfid_removed)
        self.rfid.start()

    # -- RFID callbacks (rodam em outra thread -> só ajustam estado, sem desenhar) --
    def _on_rfid_placed(self, uid):
        particle_key = RFID_MAP.get(uid)
        if particle_key and particle_key in PARTICLES:
            particle = PARTICLES[particle_key]
            self.current.on_cube_placed(particle)
        else:
            print(f"[rfid] UID desconhecido: {uid} — adicione em data/rfid_map.json")

    def _on_rfid_removed(self):
        self.current.on_cube_removed()

    def _simulate_cube(self, particle_key):
        particle = PARTICLES.get(particle_key)
        if particle:
            self.current.on_cube_placed(particle)

    def switch_screen(self, name):
        self.current_name = name
        self.current = self.screens[name]
        self.current.on_enter()

    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            t = time.time() - self.start_time

            pygame_events = pygame.event.get()
            for ev in pygame_events:
                if ev.type == pygame.QUIT:
                    self.running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        self.running = False
                    elif ev.key in MOCK_CUBE_KEYS and not self.input.using_gpio:
                        self._simulate_cube(MOCK_CUBE_KEYS[ev.key])
                    elif ev.key == pygame.K_9 and not self.input.using_gpio:
                        self.current.on_cube_removed()

            self.input.poll_pygame_events(pygame_events)

            action = self.input.get_nowait()
            while action:
                self.current.handle_input(action)
                action = self.input.get_nowait()

            self.current.update(dt)

            if self.current.next_screen and self.current.next_screen != self.current_name:
                self.switch_screen(self.current.next_screen)
            else:
                self.current.next_screen = None

            self.current.draw(self.surface, t)
            pygame.display.flip()

        self.rfid.stop()
        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
    sys.exit(0)
