# import argparse
import cv2 as cv
import screen_brightness_control as sbc
from functions import *

# parser = argparse.ArgumentParser(
#     prog = "Adaptive Brightness",
#     description = "A project made to bring the adaptive brightness to your Windows/Linux device which has a webcam",
#     add_help = 
#     """
    
#     """,
#     allow_abbrev = True,
#     exit_on_error = False
# )

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FPS, 30)
cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0) # 1=manual, 3=auto
cap.set(cv.CAP_PROP_EXPOSURE, 0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

last_brightness = -1
max_dif = 50


# print(f'cv.CAP_PROP_APERTURE : {cap.get(cv.CAP_PROP_APERTURE)}')
# print(f'cv.CAP_PROP_CONTRAST : {cap.get(cv.CAP_PROP_CONTRAST)}')
# print(f'cv.CAP_PROP_AUTO_EXPOSURE : {cap.get(cv.CAP_PROP_AUTO_EXPOSURE)}')
# print(f'cv.CAP_PROP_BACKLIGHT : {cap.get(cv.CAP_PROP_BACKLIGHT)}')
# print(f'cv.CAP_PROP_AUTO_WB : {cap.get(cv.CAP_PROP_AUTO_WB)}')
# print(f'cv.CAP_PROP_GAMMA : {cap.get(cv.CAP_PROP_GAMMA)}')
# print(f'cv.CAP_PROP_ISO_SPEEDZ : {cap.get(cv.CAP_PROP_ISO_SPEED)}')
# print(f'cv.CAP_PROP_IRIS : {cap.get(cv.CAP_PROP_IRIS)}')

while True:
    _, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(7,7), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    
    meanPixel = cv.mean(gray)[0]
    
    if abs(maxVal - meanPixel) >= max_dif:
        if (maxVal >= meanPixel):
            val = (meanPixel)
        else:
            val = maxVal
    else:
        val = (maxVal + meanPixel) / 2

    brightness = remap(val, 1, 25, 0, 100)
    
    brightness = round(brightness)
    if (brightness!=last_brightness):
        print(f'brightness => {brightness}')
        sbc.fade_brightness(
            brightness,
            force=True,
            increment=1,
            interval=0.01,
            blocking=True
        )

    # cv.imshow('out', gray)

    if cv.waitKey(1000) | 0xff == ord('q'):
        break
    last_brightness = brightness

cap.close()
cv.destroyAllWindows()