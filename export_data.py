import cv2

def FrameCapture(path):
    video1p = cv2.VideoCapture(path)
    count = 0
    success = 1
    while success:
        success, image = video1p.read()
        if count % 50 == 0:
            cv2.imwrite("images\\frame%d.jpg" % (count / 50), image)
        count += 1

if __name__ == '__main__':
    FrameCapture("C:\\Users\\SY TRUONG\\Downloads\\Bottles\\Video12p.mp4")
