import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 99
LED_PIN = 13
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 1



#
#   building the strip with configurations 
#

strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL
)

strip.begin()


def teste(nome, r, g, b):
    print(f"{nome}: ({r}, {b}, {g})")

    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(r, b, g))

    strip.show()
    time.sleep(2)


try:
    teste("VERMELHO", 255, 0, 0)
    teste("VERDE",    0, 255, 0)
    teste("AZUL",     0, 0, 255)

    # combinações
    teste("AMARELO",  255, 255, 0)
    teste("CIANO",    0, 255, 255)
    teste("MAGENTA",  255, 0, 255)
    teste("BRANCO",   255, 255, 255)

finally:
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()