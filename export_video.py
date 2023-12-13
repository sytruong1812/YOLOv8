import cv2

def FrameCapture(path):
    video = cv2.VideoCapture(path)
    count = 0
    success = 1
    while success:
        success, image = video.read()
        if count % 10 == 0:
            cv2.imwrite("C:\\Users\\SY TRUONG\\Downloads\\YOLOv8\\images\\frame%d.jpg" % (count / 10), image)
        count += 1

if __name__ == '__main__':
    FrameCapture("C:\\Users\\SY TRUONG\\Videos\\video_new.mp4")
