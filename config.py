"""
Configurações do fliperama de Partículas Elementares.
Ajuste os pinos GPIO e resolução de acordo com sua montagem.
"""

# ---------------------------------------------------------------------------
# TELA — TV vertical, 1080x1920 (largura x altura, já em pé)
# ---------------------------------------------------------------------------
FULLSCREEN = True
# Com FULLSCREEN=True a resolução é detectada automaticamente (vai bater
# com 1080x1920 assim que rodar conectado na TV). Estes valores abaixo só
# valem para testar em modo janela (FULLSCREEN=False) no PC.
WINDOW_SIZE = (540, 960)  # metade de 1080x1920, mesma proporção

# ---------------------------------------------------------------------------
# BOTÃO ÚNICO (gpiozero, pull-up interno, liga ao GND quando pressionado)
# ---------------------------------------------------------------------------
PIN_BUTTON = 17
# Toque curto = confirmar (A). Segurar mais que isso = voltar (B).
LONG_PRESS_SECONDS = 0.5


# ---------------------------------------------------------------------------
# JOYSTICK ANALÓGICO BASE BOTÕES 
# ---------------------------------------------------------------------------
BTN_CIMA = 24
BTN_BAIXO = 27
BTN_ESQUERDA = 22
BTN_DIREITA = 23


# ---------------------------------------------------------------------------
# LEITOR RFID (MFRC522 via SPI)
# ---------------------------------------------------------------------------
RFID_ENABLED = True
# Tempo (segundos) sem leitura bem sucedida até considerarmos que o cubo
# foi retirado do leitor.
RFID_REMOVE_TIMEOUT = 0.6
# Intervalo entre tentativas de leitura
RFID_POLL_INTERVAL = 0.30

# ---------------------------------------------------------------------------
# MODO DESENVOLVIMENTO (roda no PC, sem Raspberry/GPIO/RFID/joystick reais)
# Detectado automaticamente: se gpiozero não estiver disponível, o teclado
# assume o controle:
#   setas = cima/baixo/esquerda/direita, ENTER/ESPAÇO = A, ESC/BACKSPACE = B
#   teclas 1-8 = simulam encostar um cubo diferente no leitor
# ---------------------------------------------------------------------------

FPS = 30
