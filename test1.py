import csv
import time
import os
import board
import adafruit_bmp3xx
from gpiozero import LED

# device setup
GPIO_PIN = 27
i2c = board.I2C() # uses board.SCL and board.SDA
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
pin = LED(GPIO_PIN)
init_altitude = bmp.altitude
altitude_list = []

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

# CSV setup
csv_file_path = "bmp_data.csv"
headers = ["altitude", "pressure", "temperature"]
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

while True:
    # collect data
    data = [
        {"altitude": bmp.altitude, "pressure": bmp.pressure, "temperature": bmp.temperature}
    ]

    # write data to file
    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerows(data)
        print(f"Data has been appended to {csv_file_path}")
    except Exception as e:
        print(f"Error: {e}")

    if len(altitude_list) >= 10:
        altitude_list.pop(0)
    
    altitude_list.append(bmp.altitude)
    print("altitude: " + str(bmp.altitude))

    # cutdown mechanism
    if bmp.altitude - init_altitude > 5 and len(altitude_list) == 10 and altitude_list[9] <= altitude_list[0] + 1:
        print("Cutdown activated")
        pin.on()
        time.sleep(4)
        pin.off()
        time.sleep(2)
        pin.on()
        time.sleep(4)
        pin.off()

    # delay between iterations (in seconds)
    time.sleep(1)
