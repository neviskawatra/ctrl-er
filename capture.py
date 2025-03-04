import cv2
import mediapipe
import vgamepad
from math_utils import Vector

mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mediapipe.solutions.drawing_utils

controller = vgamepad.VX360Gamepad()

cam = cv2.VideoCapture(0)


class Capture:
    def start(self):
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

                    index_base = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    thumb_vector = [thumb_tip.x - thumb_base.x, thumb_tip.y - thumb_base.y]
                    index_vector = [index_tip.x - index_base.x, index_tip.y - index_base.y]

                    thumb_unit_vector = Vector.unit_vector(thumb_vector)
                    index_unit_vector = Vector.unit_vector(index_vector)

                    thumb_index_angle = Vector.calculate_angle(thumb_unit_vector, index_unit_vector)
                    
                    cv2.putText(frame, f"Thumb vector: {thumb_unit_vector}", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.putText(frame, f"Index vector: {index_unit_vector}", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.putText(frame, f"Angle: {thumb_index_angle}", (50, 150), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
                    
                    if thumb_index_angle > 10:
                        scaled_thumb_index_angle_value = int(((thumb_index_angle)/90) * 255)
                        controller.right_trigger(max(0, scaled_thumb_index_angle_value) if scaled_thumb_index_angle_value <= 255 else 255)
                        controller.update()
                    else:
                        controller.right_trigger(0)
                        controller.update()
                    
            cv2.imshow("Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cam.release()
        cv2.destroyAllWindows()