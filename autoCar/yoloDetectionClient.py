import cv2
import time
import argparse
import socket

from yolo.YoloV8 import Yolov8s

def parse_args():
    parser = argparse.ArgumentParser()
 
    parser.add_argument('--showCamera',
                        type=bool,
                        default=False,
                        help='Set value to endcode view camera')

    args = parser.parse_args()
    return args

class YoloInit():
    def __init__(self, args) -> None:
        self.HOST = "127.0.0.1"
        self.PORT = 65432

        # Define socket client sent signal to server control engine
        self.driverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.HOST, self.PORT)
        print('Connecting to' + str(server_address))
        self.driverSocket.connect(server_address)
        print('Connected')

        self.showCamera = args.showCamera
        self.yolo = Yolov8s("asset/best_nms_extended.onnx", "asset/dataset.yaml" , confidence_thres=0.5, iou_thres=0.5)
        self.cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, framerate=30/1 ! nvvidconv ! video/x-raw(memory:NVMM) ! nvvidconv ! video/x-raw, format=BGRx !  videoconvert ! video/x-raw, format=BGR ! appsink', cv2.CAP_GSTREAMER)
        
    def run(self):
        while self.cap.isOpened():
            st = time.time()
            success, img = self.cap.read()
            if success:  
                _, info = self.yolo.predict(img, returnImg= self.showCamera)

                if self.showCamera:
                    #cv2.imshow("YOLOv8 Inference", _)
                    cv2.imwrite("debug.jpg", _)

                en = time.time()
                print(f"Fps: {int(1/(en-st))} - ClassID: {info[0]} - Bottom line: {info[1]}")

                if len(info[0]) > 0:
                    self.driverSocket.sendall(bytes((str(info) + "\r\n"), "utf8"))

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main = YoloInit(parse_args())
    main.run()
