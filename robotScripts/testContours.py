import numpy as np
import cv2, queue, threading

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

cap = VideoCapture(1)
while True:
  frame = cap.read()
  imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  imgray = cv2.bitwise_not(imgray)
  ret, thresh = cv2.threshold(imgray, 100, 255, 0)
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  img = np.copy(frame)

  cv2.drawContours(img, contours, -1, (0,0,255), 3)
  cv2.imshow("frame", img)
  if chr(cv2.waitKey(1)&255) == 'q':
    break