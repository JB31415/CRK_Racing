from picamera2.encoders import H264Encoder
from picamera2 import Picamera2, Preview
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time

picam2=Picamera2()
video_config = picam2.create_video_configuration(main={'size': (1920, 1080)}, lores={'size': (640, 480)})
picam2.configure(video_config)
encoder = H264Encoder(bitrate=100000)
output= 'test.h264'
picam2.start_preview(Preview.QTGL)
picam2.start_recording(encoder, output)
time.sleep(20)
picam2.stop_recording()
picam2.stop_preview()





while True:#This loops is a continous loop such that it does not stop scanning unless told to
    
    ret,frame=cap.read()#ret is boolean whihc means it tell us whether the fram was successfully captured,
    #frame, containts the image data
    
    for barcode in decode(frame):#decode(frame), is used to detect barcodes withing the frame
        print(barcode.data)#is the data from the qr code
        myData=barcode.data.decode('utf-8')#.decode('utf-8) converts it to a readible string format
        print(myData)
        
        #send the decoded data to the other script via socket
        # server.sendall(myData.encode('utf-8'))
        
        
        pts=np.array([barcode.polygon],np.int32)#barcode.polygon, return the corrdinate of the corners of the detected qr code
       #np.array([barcode.polygon],np.int32), converts the polygon data into a numpy array, whihc is needed by opencb for drawwing
       
       #cv.polylines, draw the outline of the barcode on the frame
        cv.polylines(frame,[pts],True,(255,0,0),5)
        pts2=barcode.rect#Gets teh bounding box of the qr code
        
        #putText, write the decoded data, qr code tect, on the video frame at the position defined by pts2[0],pts2[1]
        cv.putText(frame,myData,(pts2[0],pts2[1]), cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv.imshow('Scanning',frame)#Displays the video feed
    if cv.waitKey(1) & 0xFF == ord('q'):#
        break





