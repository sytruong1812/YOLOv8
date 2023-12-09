from drivers.CarDriver import CarDriver_SocketServer
from drivers.PCA9685 import PCA9685_I2C

class AutoCar():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 12345

        # Define socket server receive signal for control car engine; run socket over Process
        self.carDrver = CarDriver_SocketServer(self.HOST, self.PORT)
        self.carDrver.engine = PCA9685_I2C(ENA_Connec2PinPWM=0,
                 IN1_Connec2PinPWM=1,
                 IN2_Connec2PinPWM=2,
                 Servo_Connec2Channel=3)

if __name__ == '__main__':
    main = AutoCar()
    main.carDrver.Run()
