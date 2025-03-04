import cv2
import mediapipe
import vgamepad
import threading
from math_utils import Vector


class Capture:
    def __init__(self):
        self.mp_hands = mediapipe.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mediapipe.solutions.drawing_utils

        self.controller = vgamepad.VX360Gamepad()

        self.cam = cv2.VideoCapture(0)

        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_frames, daemon=True)
        self.capture_thread.start()

    def capture_frames(self):
        while self.running:
            is_frame, frame = self.cam.read()
            if not is_frame:
                continue
            frame = cv2.flip(frame, 1)

            with self.lock:
                self.frame = frame

    def start(self):
        while True:
            with self.lock:
                if self.frame is None:
                    continue
                frame = self.frame.copy()

            processed_frame = self.hands.process(frame)

            if processed_frame.multi_hand_landmarks:
                for landmarks in processed_frame.multi_hand_landmarks:
                    
                    vectors = self.get_vectors(frame, landmarks)

                    # cv2.putText(frame, f"Middle vector: {vectors['middle_unit_vector']}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

                    if vectors["thumb_index_angle"] > 5:
                        scaled_thumb_index_angle_value = vectors["thumb_index_angle"] / 70
                        capped_thumb_index_angle = max(0, min(1, scaled_thumb_index_angle_value))
                        cv2.putText(frame, f"Capped val: {capped_thumb_index_angle}", (50, 150), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
                        self.controller.right_trigger_float(capped_thumb_index_angle)
                        self.controller.update()
                    else:
                        self.controller.right_trigger(0)
                        self.controller.update()
                    
                    # cv2.putText(frame, f"Index Angle: {vectors["index_angle_from_vertical_line"]}", (50, 150), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
                    
                    if vectors["index_angle_from_vertical_line"] >= 10 or vectors["index_angle_from_vertical_line"] <= -10:
                        scaled_index_vertical_angle_value = vectors["index_angle_from_vertical_line"] / 45
                        self.controller.left_joystick_float(-max(-1, min(1, scaled_index_vertical_angle_value)), 0)
                        self.controller.update()
                        
                    if vectors["middle_unit_vector"][1] > 0.5:
                        self.controller.left_trigger_float(vectors["middle_unit_vector"][1])
                        self.controller.update()
                    else:
                        self.controller.left_trigger(0)
                        self.controller.update()
                        
            else:
                self.reset_controller()
                
            cv2.imshow("Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break
            
        self.cam.release()
        cv2.destroyAllWindows()
        
    def get_vectors(self, frame, landmarks):
        self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        thumb_base = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC]
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]

        index_base = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        
        middle_base = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        thumb_vector = [thumb_tip.x - thumb_base.x, thumb_tip.y - thumb_base.y]
        index_vector = [index_tip.x - index_base.x, index_tip.y - index_base.y]
        middle_vector = [middle_tip.x - middle_base.x, middle_tip.y - middle_base.y]

        thumb_unit_vector = Vector.unit_vector(thumb_vector)
        index_unit_vector = Vector.unit_vector(index_vector)
        middle_unit_vector = Vector.unit_vector(middle_vector)

        thumb_index_angle = Vector.calculate_angle(thumb_unit_vector, index_unit_vector)
        
        index_angle_from_vertical_line = Vector.calculate_signed_angle(index_unit_vector, Vector.POS_Y_UNIT)
        
        return {
            "thumb_index_angle" : thumb_index_angle,
            "thumb_unit_vector" : thumb_unit_vector,
            "index_unit_vector" : index_unit_vector,
            "index_angle_from_vertical_line" : index_angle_from_vertical_line,
            "middle_unit_vector" : middle_unit_vector
        }

    def reset_controller(self):
        self.controller.right_trigger(0)
        self.controller.left_trigger(0)
        self.controller.left_joystick_float(0, 0)
        self.controller.update()

    def stop(self):
        self.running = False
        self.cam.release()

if __name__ == "__main__":
    input_capture = Capture()
    input_capture.start()