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
  frame = cv2.flip(frame, 1, frame)
  imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  imgray = cv2.bitwise_not(imgray)
  ret, thresh = cv2.threshold(imgray, 120, 255, 0)
  #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  img = np.copy(frame)
  imgThirdSize = int(len(thresh[0])/3)

  #line pos
  n = imgThirdSize
  val = 0
  landon = 0
  
  while n < (imgThirdSize * 2):
    if thresh[500][n] == 255:
      val += n
      landon += 1
    n += 1
  if landon > 0:
    val /= landon
    val = int(val)
  else:
    val = None
  print(val)
  print(landon)
  if landon > 200:
    print("LANDON AITKEN LING WHAT ARE YOU DOING")
  
  #green square
  landon2 = 0
  n = imgThirdSize
  greenVal = 0
  greenPos = 800
  while n < (imgThirdSize * 2):
    if img[greenPos][n][1] >= img[greenPos][n][0] + 20 and img[greenPos][n][1] >= img[greenPos][n][2] + 20:
      greenVal += n
      landon2 += 1
    n += 1
  if landon2 > 0:
    greenVal /= landon2
    greenVal = int(greenVal)
  else:
    greenVal = None
    n += 1

  #cv2.drawContours(img, contours, -1, (0,0,255), 3)
  img = cv2.line(img, (0, 500), (len(thresh[0]), 500), (0, 255, 0), 3)
  img = cv2.line(img, (0, greenPos), (len(thresh[0]), greenPos), (0, 0, 255), 3)
  if val != None:
    img = cv2.circle(img, (val, 500), 10, (255, 0, 0), 5)
  if greenVal != None:
    img = cv2.circle(img, (greenVal, greenPos), 10, (255, 0, 0), 5)
  
  cv2.imshow("frame", img)
  if chr(cv2.waitKey(1)&255) == 'q':
    break