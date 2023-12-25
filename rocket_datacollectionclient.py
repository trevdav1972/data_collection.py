import time
import math
from smbus2 import SMBus
from MPU6050 import MPU6050
import RPi.GPIO as GPIO
import socket 

HOST = 'whatever the ip is'
PORT = 'whatever port  you want'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

bus = SMBus(1)  # Use I2C bus 1
address = 0x68  # MPU6050 address

mpu = MPU6050(bus, address)

servo1_pin = 9
servo2_pin = 10
servo3_pin = 11
servo4_pin = 12
servo5_pin = 8
servo6_pin = 7
servo7_pin = 6
servo8_pin = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(servo3_pin, GPIO.OUT)
GPIO.setup(servo4_pin, GPIO.OUT)
GPIO.setup(servo5_pin, GPIO.OUT)
GPIO.setup(servo6_pin, GPIO.OUT)
GPIO.setup(servo7_pin, GPIO.OUT)
GPIO.setup(servo8_pin, GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)
servo2 = GPIO.PWM(servo2_pin, 50)
servo3 = GPIO.PWM(servo3_pin, 50)
servo4 = GPIO.PWM(servo4_pin, 50)
servo5 = GPIO.PWM(servo5_pin, 50)
servo6 = GPIO.PWM(servo6_pin, 50)
servo7 = GPIO.PWM(servo7_pin, 50)
servo8 = GPIO.PWM(servo8_pin, 50)

servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)
servo5.start(0)
servo6.start(0)
servo7.start(0)
servo8.start(0)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_servo_angle(servo, angle):
    duty = map_value(angle, 0, 180, 2, 12)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.05)

try:
    mpu.set_accel_range(mpu.ACCEL_RANGE_8G)
    mpu.set_gyro_range(mpu.GYRO_RANGE_500DEG)
    
    while True:
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()

        angle_x = math.degrees(math.atan2(accel_data['y'], math.sqrt(accel_data['x']**2 + accel_data['z']**2)))
        angle_y = math.degrees(math.atan2(accel_data['x'], math.sqrt(accel_data['y']**2 + accel_data['z']**2)))

        # Create a list with gyroscope and accelerometer data
        data_list = [
            gyro_data['x'],
            gyro_data['y'],
            accel_data['x'],
            accel_data['y'],
            accel_data['z']
        ]
        
        # Convert the list to a string for transmission
        data_str = ','.join(map(str, data_list))

        # Send the data string over the socket
        sock.sendall(data_str.encode())

        time.sleep(0.1)

        # Convert the list to a string for transmission
        data_str = ','.join(map(str, data_list))

        # Send the data string over the socket
        sock.sendall(data_str.encode())


        print("Angle X: ", angle_x)
        print("Angle Y: ", angle_y)

        # Servo 1 (Roll)
        if -1 < angle_x < 1: ## if angle_x < 1 and angle_x > -1:
            set_servo_angle(servo2, 90)
        else: ## if angle_x > 1:
            set_servo_angle(servo2, 90 - angle_y)
        
        if angle_x == 0:
            set_servo_angle(servo1, 90)
        else: ## if angle != 0:
            set_servo_angle(servo1, 90 + angle_y)

        if angle_x == 0:
            set_servo_angle(servo6, 10)
        else: ## if angle_x != 0:
            set_servo_angle(servo6, 10 + angle_y)
        
        # Servo 2 (Pitch)
        if angle_y == 0:
            set_servo_angle(servo3, 90)
        else: ## if angle_y != 0:
            set_servo_angle(servo3, 90 + angle_x)
        
        if angle_y == 0:
            set_servo_angle(servo4, 90)
        else: ## if angle_y != 0:
            set_servo_angle(servo4, 90 - angle_x)
        
        if angle_y == 0:
            set_servo_angle(servo5, 10)
        else: ## if angle_y != 0:
            set_servo_angle(servo5, 10 - angle_x)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    servo1.stop()
    servo2.stop()
    servo3.stop()
    servo4.stop()
    servo5.stop()
    servo6.stop()
    servo7.stop()
    servo8.stop()
    GPIO.cleanup()
    sock.close()
