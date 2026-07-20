# Creating and Managing window
import time
import cv2 as cv
import sys

# creating window
cv.namedWindow("MY window", flags=400)

# resize the window
cv.resizeWindow("MY window", width=300, height=400)

# moving the windows position
cv.moveWindow("MY window", x=100, y=200)

# display an image
img = cv.imread("opencv_demo/sample.png", flags=10)

if img is None:
    sys.exit("Image not found")

# show image
img = cv.resize(img, (400, 400), interpolation=cv.INTER_LINEAR)
cv.imshow("My Image", img)

time.sleep(2)

# destory specfic window 
cv.destroyWindow("MY window")

time.sleep(2)

# destory all windows
# cv.destroyAllWindows()


# wait key (until this key is not pressed window won't close)
cv.waitKey(0)