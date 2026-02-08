import cv2
import mediapipe as mp

#setup media pipe hands 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1) #as we eed only 1 hand
mp_draw = mp.solutions.drawing_utils

#setup the camera
cap=cv2.VideoCapture(0)

while True:
    success , img = cap.read()
    if not success:
        break

img= cv2.flip(img,1) #flip the image to get mirror view
img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #mediapipe works with RGB images
results = hands.process(img_rgb) #process the image to find hands

if results.multi_hand_landmarks: #if hands are detected
    for hand_landmarks in results.multi_hand_landmarks:
        h ,w , c = img.shape #get the dimensions of the image
        index_tip=hand_landmarks.landmark[08] #get the index finger tip landmark
        cx , cy= int(index_tip.x * w) , int(index_tip.y * h) #convert the normalized coordinates to pixel coordinates
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED) #draw a circle at the index finger tip
        
cv2.imshow("Fruit Ninja CV",img) #display the image
if cv2.waitKey(1) & 0xFF == ord('q'): #exit on 'q' key press
    break
cap.release()
cv2.destroyAllWindows()
