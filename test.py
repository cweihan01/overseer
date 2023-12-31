import time
import board
import adafruit_bmp3xx

# I2C setup
i2c = board.I2C()
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

#from digitalio import DigitalInOut, Direction
#spi = board.SPI()
#cs = DigitalInOut(board.D5)
#bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

while True:
    print(
        "Pressure: {:6.4f}  Temperature: {:5.2f}".format(bmp.pressure, bmp.temperature)
    )
    time.sleep(1)
