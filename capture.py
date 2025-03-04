import cv2
import mediapipe

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
            
    cv2.imshow("Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()