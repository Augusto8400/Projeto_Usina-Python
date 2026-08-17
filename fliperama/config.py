"""
Configurações do fliperama de Partículas Elementares.
Ajuste os pinos GPIO e resolução de acordo com sua montagem.
"""

# ---------------------------------------------------------------------------
# TELA (TV em pé / vertical)
# ---------------------------------------------------------------------------
FULLSCREEN = True
# Se FULLSCREEN=True, a resolução é detectada automaticamente.
# Use estes valores só para testar em modo janela (FULLSCREEN=False).
WINDOW_SIZE = (540, 960)  # metade de 1080x1920, só para debug no monitor do PC

# ---------------------------------------------------------------------------
# BOTÕES (gpiozero, pull-up interno, botão liga ao GND quando pressionado)
# ---------------------------------------------------------------------------
PIN_UP = 5
PIN_DOWN = 6
PIN_LEFT = 13
PIN_RIGHT = 19
PIN_A = 26       # confirmar / selecionar
PIN_B = 21       # voltar

# ---------------------------------------------------------------------------
# LEITOR RFID (MFRC522 via SPI)
# ---------------------------------------------------------------------------
RFID_ENABLED = True
# Tempo (segundos) sem leitura bem sucedida até considerarmos que o cubo
# foi retirado do leitor.
RFID_REMOVE_TIMEOUT = 0.6
# Intervalo entre tentativas de leitura
RFID_POLL_INTERVAL = 0.15

# ---------------------------------------------------------------------------
# MODO DESENVOLVIMENTO (roda no PC, sem Raspberry/GPIO/RFID reais)
# Ative com a variável de ambiente FLIPERAMA_MOCK=1, ou deixe automático:
# o programa detecta se gpiozero/mfrc522 estão disponíveis.
# No modo mock, o teclado controla o jogo:
#   setas = cima/baixo/esquerda/direita, ENTER = A, ESC/BACKSPACE = B
#   teclas 1-8 = simulam encostar um cubo diferente no leitor
# ---------------------------------------------------------------------------

FPS = 30
