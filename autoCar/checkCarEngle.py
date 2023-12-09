from drivers.PCA9685 import PCA9685_I2C

engine = PCA9685_I2C(ENA_Connec2PinPWM=0, IN1_Connec2PinPWM=1, IN2_Connec2PinPWM=2, Servo_Connec2Channel=3)
# engine.Servo_Angle(1) #trai
# engine.Servo_Angle(90) #giua
engine.Servo_Angle(180) #phai
# engine.DC_Stop(True)