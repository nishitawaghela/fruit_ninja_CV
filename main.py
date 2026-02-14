import cv2
import mediapipe as mp
import random

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Setup Camera
cap = cv2.VideoCapture(0)

WIDTH, HEIGHT = 640, 480
GRAVITY = 0.2
fruits = []

def spawn_fruit():
    fruit = {
        'x': random.randint(100, WIDTH - 100),
        'y': HEIGHT,
        'vx': random.randint(-4, 4),
        'vy': -random.randint(12, 18),
        'color': (0, 165, 255)
    }
    return fruit

while True:
    success, img = cap.read()
    if not success:
        break

    
    # We flip immediately so all our drawing happens on the "mirrored" version
    img = cv2.flip(img, 1)

    
    # 1. Hand Detection Logic
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    index_finger_tip = None # Store coordinate for collision check later

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = img.shape
            
            
            index_tip = hand_landmarks.landmark[8] # Use 8, not 08
            
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            
            # Save this position to check for cuts!
            index_finger_tip = (cx, cy)

    # 2. Fruit Physics Logic
    if random.randint(0, 100) < 2:
        fruits.append(spawn_fruit())

    for fruit in fruits[:]: 
        fruit['x'] += fruit['vx']
        fruit['y'] += fruit['vy']
        fruit['vy'] += GRAVITY

        if fruit['y'] > HEIGHT:
            fruits.remove(fruit)
        else:
            cv2.circle(img, (int(fruit['x']), int(fruit['y'])), 30, fruit['color'], cv2.FILLED)
            
            
            
    cv2.imshow("Fruit Ninja CV", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()