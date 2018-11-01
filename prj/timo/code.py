
import cv2
import numpy as np
import servobot

breedte = 640
hoogte = 480
breedte_klein = breedte / 4
hoogte_klein = hoogte / 4
servo = servobot.servo()
servo_x = 40
servo.set_angle(servo_x)
cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
if cascade.empty(): raise Exception("your cascade is empty. are you sure, the path is correct ?")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("your input:0 could not be opened !")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, breedte)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hoogte)
cap.set(cv2.CAP_PROP_FPS, 10)

while cap.isOpened():
  r,img = cap.read()
  if r==False: break
  gray_img = cv2.cvtColor(cv2.resize(img, (breedte_klein,hoogte_klein))
  ,cv2.COLOR_BGR2GRAY)
  rows,cols = gray_img.shape[:2]
  M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
  r_img = cv2.warpAffine(gray_img,M,(cols,rows))
  faces = cascade.detectMultiScale(r_img)
  if len(faces) > 0:
    face = (cascade.detectMultiScale(r_img))[0]
    cv2.rectangle(r_img, (face[0],face[1]), (face[0]+face[2],face[1]+face[3]), (0x00,0x00,0xff), 2)
    x1 = (((face[0],face[1])))[0]
    x2 = (((face[0]+face[2],face[1]+face[3])))[0]
    x = x1 + (x2 - x1) / 2
    if x < breedte_klein / 2:
      servo_x = servo_x + 1
    else:
      servo_x = servo_x - 1
  servo.set_angle(servo_x)
  cv2.imshow('mywin',r_img)
  if cv2.waitKey(40) == ord('q'):
    break
cv2.destroyAllWindows()