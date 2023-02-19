# motor1: left
# motor2: right

import time
import board
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

def stop():
    print("Stop.")
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0
    time.sleep(2.5)


for _ in range(1):
    print("Driving forward.")
    kit.motor1.throttle = +1.0
    kit.motor2.throttle = +1.0
    time.sleep(2.5)
    stop()

    print("Driving backward.")
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = -1.0
    time.sleep(2.5)
    stop()

    print("Turning left.")
    kit.motor1.throttle = -1.0
    kit.motor2.throttle = +1.0
    time.sleep(2.5)
    stop()

    print("Turning right.")
    kit.motor1.throttle = +1.0
    kit.motor2.throttle = -1.0
    time.sleep(2.5)
    stop()
