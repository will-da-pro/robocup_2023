import cv2

while True:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret:
        cv2.imshow("Video Capture", frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break