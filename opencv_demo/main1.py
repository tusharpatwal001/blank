import cv2 as cv
import sys

# read an image
img = cv.imread("opencv_demo/sample.png")


# Check if image was loaded successfully
if img is None:
    sys.exit("Could not read the image.")

img = cv.resize(img, (200, 200), interpolation=cv.INTER_LINEAR)


# Display the image in a window
cv.imshow("Display window", img)
k = cv.waitKey(0)  # Wait for a keystroke

# Save image if 's' key is pressed
if k == ord("s"):
    cv.imwrite("starry_night.png", img)
