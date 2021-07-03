import cv2
import mediapipe as mp
import time
import re
regex = r"\{(.*?)\}"
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

def insert_comma(string, index):
    return string[:index] + ',' + string[index:]
# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=6)
cap = cv2.VideoCapture('m5.mp4')
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
    listx=[]
    listy=[]
    matches = re.finditer(regex, str(hand_landmarks), re.MULTILINE | re.DOTALL)
    for matchNum, match in enumerate(matches):
       for groupNum in range(0, len(match.groups())):
            str1 = match.group(1)
            str2 = re.sub(r"[\n\t\s]*", "", str1)
            str3 = insert_comma(str2, str2.find('y'))
            str4 = insert_comma(str3, str3.find('z'))
            str5 = insert_comma(str4, str4.find('v'))
            str6 = insert_comma(str5, str5.find('p'))
            result = re.search('x:(.*),y:', str6)
            listx.append(float(result.group(1)))
            result = re.search(',y:(.*),z:', str6)
            listy.append(float(result.group(1)))

    print(listx)
    print(len(listx))
    print(listy)
  # cv2.imshow('MediaPipe Hands', image)
    if listy[0]>listy[5]>listy[6]>listy[7]>listy[8] and listy[0]>listy[9]>listy[10]>listy[11]>listy[12] and listy[0]>listy[13]>listy[14]>listy[15]>listy[16] and listy[0]>listy[17]>listy[18]>listy[19]>listy[20]:
        cv2.putText(image,'palm!', 
    (10,100), 
    cv2.FONT_HERSHEY_SIMPLEX, 
    4,
    (0,0,255),
    2)
  resized_image = cv2.resize(image, (800, 400)) 
  cv2.imshow('MediaPipe Hands', resized_image)
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
