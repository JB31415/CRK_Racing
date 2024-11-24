from picamera2.encoders import H264Encoder
from picamera2 import Picamera2, Preview
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time

# Initialize Picamera2
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={'size': (1920, 1080)}, lores={'size': (640, 480)})
picam2.configure(video_config)

# Initialize encoder for video recording
encoder = H264Encoder(bitrate=100000)
output = 'test.h264'

# Start preview
picam2.start_preview(Preview.QTGL)
picam2.start_recording(encoder, output)

# Capture frames and decode QR codes
start_time = time.time()
while time.time() - start_time < 30:  # Capture for 20 seconds
    frame = picam2.capture_array()
    
    # Decode QR codes in the frame
    qr_codes = decode(frame)
    for qr_code in qr_codes:
        (x, y, w, h) = qr_code.rect
        # Draw rectangle around QR code
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Get data from QR code and display on frame
        qr_data = qr_code.data.decode('utf-8')
        cv.putText(frame, qr_data, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"QR Code detected: {qr_data}")

    # Display frame
    cv.imshow('QR Code Detection', frame)
    
    # Press 'q' to exit before 20 seconds if desired
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Stop recording and preview
picam2.stop_recording()
picam2.stop_preview()
cv.destroyAllWindows()
