import socket
from drivers.PCA9685 import PCA9685_I2C

class CarDriver_SocketServer():
    def __init__(self, HOST = "127.0.0.1", PORT = 12345) -> None:
        self.HOST = HOST # Socket local IP
        self.PORT = PORT # Socket Port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))

        self.engine = PCA9685_I2C(ENA_Connec2PinPWM=0, IN1_Connec2PinPWM=1, IN2_Connec2PinPWM=2, Servo_Connec2Channel=3)

        # ['do', 'vang', 'xanh', 'xe', 'nguoi',]
        self.id_stop = {0,1,3,4} # bao gom danh sach object khi xuat hien phai stop
        self.id_run = {2} # bao gom danh sach object khi xuat hien co the run

        self.red_line_forStop = 400  # gới hạng cạnh dưới, để khi cạnh dưới của vật chạm thì dừng lại

        self.frame_couter = 0
        self.enable_couter = False
        self.after_x_frame_so_turn_left = 200 #sau 200 frame thì quẹo trái 
        self.number_frame_for_turn_left = 30 #quẹo trái trong 30 fram tiếp theo,
        self.number_frame_go_straight = 200 # hết 30 fram thì đi thẳng 200 frame
        
    def Run(self):
        while True:
            print("Server ready, waitting connection")

            self.s.listen()
            conn, addr = self.s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    _data = conn.recv(1024)

                    if not _data:
                        print(f"{addr} disconnect")
                        break

                    _data = _data.decode("utf8").splitlines()
                    print(type(_data), _data)
                    for data in _data:
                        data = list(eval(data))
                        print(data)
                        ids = data[0]  # danh sach object
                        bottomLine = data[1] # danh sach toa do canh duoi cua object
                        
                        objId_Stop = list(set(ids).intersection(self.id_stop)) # phép tính giao

                        if len(objId_Stop) >= 1:
                            print("Stop")
                            for objId in objId_Stop:
                                object_bottomLine = bottomLine[ids.index(objId)]
                                if object_bottomLine >= self.red_line_forStop:
                                    print("Stopping")
                                    self.engine.DC_Stop(True)
                                    self.frame_couter = 0
                                    self.enable_couter = False

                        elif len(set(ids).intersection(self.id_run)) >= 1:
                            print("Run")
                            self.engine.DC_Forward(True)
                            self.enable_couter = True # kích hoạt bộ đếm

                        if self.enable_couter: # chỉ khi xuất hiện đèn xanh mới thực hiện couter
                            self.frame_couter += 1
                            if self.frame_couter == self.after_x_frame_so_turn_left:
                                print("Turning left")
                                self.engine.Servo_Angle(1)
                            elif self.frame_couter == (self.after_x_frame_so_turn_left + self.number_frame_for_turn_left):
                                self.engine.Servo_Angle(90)
                            elif self.frame_couter == (self.after_x_frame_so_turn_left + self.number_frame_for_turn_left + self.number_frame_go_straight):
                                self.engine.DC_Stop(True)
                                self.frame_couter = 0 # reset số frame về 0
                                self.enable_couter = False  # ngắt bộ đếm

