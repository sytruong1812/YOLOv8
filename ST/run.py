import cv2
import time
import argparse
from yolo.YoloV8 import Yolov8s

def parse_args():
    parser = argparse.ArgumentParser()
 
    parser.add_argument('--showCamera',
                        type=bool,
                        default=False,
                        help='Set value to endcode view camera')

    args = parser.parse_args()
    return args

class ST():
    def __init__(self, args) -> None:
        self.showCamera = args.showCamera
        self.yolo = Yolov8s("/home/teddy/ST/asset/best_nms_extended.onnx", "/home/teddy/ST/asset/dataset.yaml" , confidence_thres=0.5, iou_thres=0.5)
        self.cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, framerate=30/1 ! nvvidconv ! video/x-raw(memory:NVMM) ! nvvidconv ! video/x-raw, format=BGRx !  videoconvert ! video/x-raw, format=BGR ! appsink', cv2.CAP_GSTREAMER)
        pass

    def run(self):
        while self.cap.isOpened():
            st = time.time()
            success, img = self.cap.read()
            if success:  
                _, classids = self.yolo.predict(img, returnImg= self.showCamera)
                if self.showCamera:
                    cv2.imshow("YOLOv8 Inference", _)
                en = time.time()
                print(f"Fps: {int(1/(en-st))} - ClassID: {classids}")
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main = ST(parse_args())
    main.run()
