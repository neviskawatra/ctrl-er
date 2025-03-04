import cv2
import mediapipe
from math_utils import Vector

mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mediapipe.solutions.drawing_utils

cam = cv2.VideoCapture(0)

while cam.isOpened():
    is_frame, frame = cam.read()
    if not is_frame: 
        break
    
    frame = cv2.flip(frame, 1)
    
    processed_frame = hands.process(frame)

    if processed_frame.multi_hand_landmarks:
        for landmarks in processed_frame.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            thumb_base = landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] 
            
            thumb_vector = [thumb_base.x - thumb_tip.x, thumb_base.y - thumb_tip.y]
            unit_vector = Vector.unit_vector(thumb_vector)
            
            cv2.putText(frame, f"Thumb vector: {unit_vector}", (50, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
            
    cv2.imshow("Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()