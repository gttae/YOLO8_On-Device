import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import cvzone


model=YOLO('yolov8n.pt')


cap=cv2.VideoCapture(0)


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n") 
#print(class_list)

count=0

while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(640,480))
   
    results=model.predict(frame)
 #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
#    print(px)
    list=[]         
    for index,row in px.iterrows():
#        print(row)
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'person' in c:

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),1)
            cvzone.putTextRect(frame, f'{c}', (x1,y1),1,1)

    cv2.imshow('YoloV8_detection', frame)
    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()

