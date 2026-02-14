import cv2
import mediapipe as mp
import random
import math
from collections import deque

# --- SETUP ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Use camera 1 (or 0 if 1 fails)
cap = cv2.VideoCapture(1) 

WIDTH, HEIGHT = 640, 480
GRAVITY = 0.25 # Increased Gravity slightly for faster feel

FRUIT_COLORS = [
    (0, 0, 255), (0, 255, 0), (0, 165, 255), 
    (0, 255, 255), (128, 0, 128)
]

fruits = []
particles = []
blade_trail = deque(maxlen=20) 

def spawn_fruit():
    """Spawns fruit from a random edge with velocity towards the center."""
    side = random.randint(0, 3) # 0=Left, 1=Right, 2=Top, 3=Bottom
    
    # Defaults
    x, y, vx, vy = 0, 0, 0, 0
    
    if side == 0: # LEFT WALL
        x = 0
        y = random.randint(100, HEIGHT - 100)
        vx = random.randint(10, 18)   # FAST right
        vy = random.randint(-10, 5)   # Random Up/Down arc
        
    elif side == 1: # RIGHT WALL
        x = WIDTH
        y = random.randint(100, HEIGHT - 100)
        vx = -random.randint(10, 18)  # FAST left
        vy = random.randint(-10, 5)   # Random Up/Down arc
        
    elif side == 2: # TOP WALL
        x = random.randint(100, WIDTH - 100)
        y = -50 # Start slightly above screen
        vx = random.randint(-5, 5)
        vy = random.randint(5, 12)    # FAST down
        
    else: # BOTTOM WALL (Classic)
        x = random.randint(100, WIDTH - 100)
        y = HEIGHT
        vx = random.randint(-6, 6)
        vy = -random.randint(18, 25)  # EXTRA HIGH toss
        
    return {'x': x, 'y': y, 'vx': vx, 'vy': vy, 'color': random.choice(FRUIT_COLORS)}

def spawn_explosion(x, y, color):
    for _ in range(12): # More particles for bigger boom
        particles.append({
            'x': x, 'y': y,
            'vx': random.randint(-15, 15), # Faster explosion
            'vy': random.randint(-15, 15),
            'life': 12, 'color': color
        })

# --- MAIN LOOP ---
while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    # 1. Update Blade Trail
    index_finger_tip = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = img.shape
            index_tip = hand_landmarks.landmark[8]
            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            
            index_finger_tip = (cx, cy)
            blade_trail.appendleft(index_finger_tip)
    else:
        blade_trail.clear()

    # 2. Draw Blade Trail
    for i in range(1, len(blade_trail)):
        if blade_trail[i-1] is None or blade_trail[i] is None: continue
        thickness = int(25 * (1 - i / len(blade_trail)))
        cv2.line(img, blade_trail[i-1], blade_trail[i], (255, 255, 255), thickness)

    # 3. Spawn Logic (Increased chance to 4% for chaos)
    if random.randint(0, 100) < 4:
        fruits.append(spawn_fruit())

    # 4. Update Fruits
    for fruit in fruits[:]: 
        fruit['x'] += fruit['vx']
        fruit['y'] += fruit['vy']
        fruit['vy'] += GRAVITY

        # Check Collision
        sliced = False
        if index_finger_tip:
            dist = math.hypot(index_finger_tip[0] - fruit['x'], index_finger_tip[1] - fruit['y'])
            if dist < 45: 
                spawn_explosion(fruit['x'], fruit['y'], fruit['color'])
                fruits.remove(fruit)
                sliced = True
                continue 
        
        # New Boundary Check (Delete if it flies off ANY side)
        if (fruit['y'] > HEIGHT + 50 or fruit['y'] < -100 or 
            fruit['x'] < -100 or fruit['x'] > WIDTH + 100):
            fruits.remove(fruit)
        else:
            if not sliced:
                cv2.circle(img, (int(fruit['x']), int(fruit['y'])), 30, fruit['color'], cv2.FILLED)

    # 5. Update Particles
    for p in particles[:]:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['life'] -= 1
        if p['life'] <= 0:
            particles.remove(p)
        else:
            cv2.circle(img, (int(p['x']), int(p['y'])), 5, p['color'], cv2.FILLED)

    cv2.imshow("Fruit Ninja CV", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()