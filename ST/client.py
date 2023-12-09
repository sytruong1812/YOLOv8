import time
import socket
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
import adafruit_motor.servo

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Initialize IP and PORT.")
client_socket.connect(('127.0.0.1', 12345))
client_socket.sendall('Connected'.encode('utf-8'))    # Send connected status
print("Connected to the server.")

class Control():
    def __init__(self, ENA=0, IN1=1, IN2=2, Servo1=3, Servo2=4):
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c_bus)
        self.pca.frequency = 30  # Set the PWM frequency

        self.ENA = self.pca.channels[ENA]  # Connect PWM0 to pin ENA of L298
        self.IN1 = self.pca.channels[IN1]  # Connect PWM1 to pin IN1 of L298
        self.IN2 = self.pca.channels[IN2]  # Connect PWM2 to pin IN2 of L298

        self.servo1 = self.pca.channels[Servo1]  # Connect channel 3 to servo1
        self.servo2 = self.pca.channels[Servo2]  # Connect channel 4 to servo2
        self.servo1_instance = adafruit_motor.servo.Servo(self.servo1)
        self.servo2_instance = adafruit_motor.servo.Servo(self.servo2)

    def Forward(self, enablePWM=True, duty_cycle_step=1000, speed=1.0):
        if enablePWM:
            for i in range(10000, 0xffff, duty_cycle_step):
                self.ENA.duty_cycle = int(i * speed)
            self.ENA.duty_cycle = int(0xffff * speed)
        else:
            self.ENA.duty_cycle = int(0xffff * speed)
        self.IN1.duty_cycle = int(0xffff * speed)
        self.IN2.duty_cycle = 0

    def Backward(self, enablePWM=True, duty_cycle_step=1000, speed=1.0):
        if enablePWM:
            for i in range(10000, 0xffff, duty_cycle_step):
                self.ENA.duty_cycle = int(i * speed)
            self.ENA.duty_cycle = int(0xffff * speed)
        else:
            self.ENA.duty_cycle = int(0xffff * speed)
        self.IN1.duty_cycle = 0
        self.IN2.duty_cycle = int(0xffff * speed)

    def Stop(self, enablePWM=True):
        if enablePWM:
            for i in range(0xffff, 10000, -10000):
                self.ENA.duty_cycle = i
            self.ENA.duty_cycle = 0
        else:
            self.ENA.duty_cycle = 0
        self.IN1.duty_cycle = 0
        self.IN2.duty_cycle = 0

    def Servo1_Angle(self, angle: int):
        self.servo1_instance.angle = angle

    def Servo2_Angle(self, angle: int):
        self.servo2_instance.angle = angle

try:
    myControl = Control(ENA=0, IN1=1, IN2=2, Servo1=3, Servo2=4)
    id_stop = {0, 1, 2, 3, 4}   # info = ['Saltshaker','Glue','Lifebuoy','7up','Pepsi']
    myControl.Servo1_Angle(110)
    myControl.Servo2_Angle(30)
    while True:
        myControl.Forward(True, speed=0.2)
        response = client_socket.recv(1024)
        if not response:
            print("Empty response received from the server.")
            break
        response_str = response.decode('utf-8')

        try:
            data = eval(response_str)
        except Exception as e:
            # print(f"Error evaluating response: {e}")
            continue  # Skip processing this response

        if len(data) >= 2:
            obj, bottomLine = data[0], data[1]
            print('Response: {}\n'.format(data))
            obj_stop_ids = list(set(obj).intersection(id_stop))

            if len(obj_stop_ids) >= 1:
                print("Stopping")
                myControl.Servo2_Angle(180)
                for id in obj_stop_ids:
                    if len(obj) > id and len(bottomLine) > id and bottomLine[id] >= 150:
                        myControl.Stop(True)
                        time.sleep(5)
                        myControl.Servo2_Angle(30)
                        time.sleep(5)
                continue  # Không thoát vòng lặp khi nhận được ID của đối tượng
            elif response_str == 'Exit':
                print("Exit")
                myControl.Servo1_Angle(110)
                myControl.Servo2_Angle(30)
                myControl.Stop(True)
                client_socket.close()
                break
except KeyboardInterrupt:
    print("KeyboardInterrupt: Closing connections and exiting...")
    time.sleep(1)
    client_socket.close()
    pass
