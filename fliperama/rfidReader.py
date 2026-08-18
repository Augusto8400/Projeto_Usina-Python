import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Hold a tag near the reader to read.")
    id, text = reader.read()
    print("ID: %s" % id)
    print("Text: %s" % text.strip())
finally:
    GPIO.cleanup()
