import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 


# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=6)
cap = cv2.VideoCapture('m4.mp4')
while cap.isOpened():
  start = time.time()
  count=0
  success, image = cap.read()
  if not success:
    break

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  image.flags.writeable = False
  results = hands.process(image)
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
  c=1
  for (x,y,w,h) in faces:
      cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2) 
      cv2.putText(image, f'P{c}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
      c+=1
  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(
          image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
  cv2.imshow('MediaPipe Hands', image)
  count+=1
  if cv2.waitKey(5) & 0xFF == 27:
    break
    
end = time.time()
seconds = end - start
print("Time taken : {0} seconds".format(seconds))
fps  =count / seconds
print ("Estimated frames per second : {0}".format(fps))
hands.close()
cap.release()
