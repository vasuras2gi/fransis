# import cv2
# import time
# import sys
# import os
# import easyocr
# import face_recognition
# import threading
# import json

# # --- STANDARD MEDIAPIPE IMPORT ---
# import mediapipe as mp
# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils
# # --------------------------------

# from ultralytics import YOLO

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from memory.redis_broker import Thalamus

# class VisualCortex:
#     def __init__(self):
#         self.thalamus = Thalamus()
#         print("[VISUAL CORTEX] Loading YOLO model...")
#         self.model = YOLO('yolov8n.pt')
        
#         print("[VISUAL CORTEX] Loading Text Reader (OCR) on GPU...")
#         self.reader = easyocr.Reader(['en'], gpu=True) 
        
#         # --- NAYA: MEDIAPIPE (Hand Tracking Engine) ---
#         print("[VISUAL CORTEX] Activating Hand Tracking...")
#         self.hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
#         self.mp_draw = mp_draw
#         self.mp_hands = mp_hands
#         # ----------------------------------------------
        
#         # --- DYNAMIC FACE MEMORY ---
#         self.faces_dir = "memory/faces"
#         os.makedirs(self.faces_dir, exist_ok=True)
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.register_next_face_as = None
        
#         print("[VISUAL CORTEX] Recalling known faces from memory...")
#         for filename in os.listdir(self.faces_dir):
#             if filename.endswith(".jpg") or filename.endswith(".png"):
#                 name = os.path.splitext(filename)[0]
#                 img_path = os.path.join(self.faces_dir, filename)
#                 image = face_recognition.load_image_file(img_path)
#                 encodings = face_recognition.face_encodings(image)
#                 if encodings:
#                     self.known_face_encodings.append(encodings[0])
#                     self.known_face_names.append(name)
#         print(f"👤 [FACE MEMORY] I remember {len(self.known_face_names)} faces.")
        
#         threading.Thread(target=self.listen_for_face_commands, daemon=True).start()
            
#         print("[VISUAL CORTEX] Opening laptop camera...")
#         self.cap = cv2.VideoCapture(0)
        
#         self.last_read_time = 0 
#         self.last_broadcast_time = 0
#         self.last_face_check_time = 0
#         self.current_person_name = "person" 

#     def listen_for_face_commands(self):
#         pubsub = self.thalamus.client.pubsub()
#         pubsub.subscribe("face_registration_stream")
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 data = json.loads(message['data'])
#                 name_to_save = data.get("name")
#                 if name_to_save:
#                     self.register_next_face_as = name_to_save
#                     print(f"\n📸 [FACE CAM] ALERT: Taking a mental snapshot for '{name_to_save}' in the next frame!\n")
        
#     def process_vision(self):
#         while self.cap.isOpened():
#             ret, frame = self.cap.read()
#             if not ret:
#                 break
            
#             seen_objects = []
#             current_time = time.time()
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
#             # --- 1. DYNAMIC HAND GESTURE DETECTION ---
#             hand_results = self.hands.process(rgb_frame)
#             if hand_results.multi_hand_landmarks:
#                 for hand_landmarks in hand_results.multi_hand_landmarks:
#                     self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
#                     fingers = []
#                     tips = [8, 12, 16, 20]
                    
#                     # Thumb
#                     if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
#                         fingers.append(1)
#                     else:
#                         fingers.append(0)
                        
#                     # Other 4 fingers
#                     for tip in tips:
#                         if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
#                             fingers.append(1)
#                         else:
#                             fingers.append(0)
                            
#                     total_fingers = fingers.count(1)
#                     gesture_text = f"Hand Gesture: showing {total_fingers} fingers"
#                     if total_fingers == 0:
#                         gesture_text = "Hand Gesture: Fist (Mutthi band hai)"
#                     elif total_fingers == 5:
#                         gesture_text = "Hand Gesture: Open Palm (Khula haath)"

#                     seen_objects.append({"name": gesture_text, "confidence": 1.0})
#             # -----------------------------------------------------------------

#             # --- 2. FACE REGISTRATION ---
#             if self.register_next_face_as:
#                 face_locations = face_recognition.face_locations(rgb_frame)
#                 if face_locations: 
#                     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#                     self.known_face_encodings.append(face_encodings[0])
#                     self.known_face_names.append(self.register_next_face_as)
                    
#                     save_path = os.path.join(self.faces_dir, f"{self.register_next_face_as}.jpg")
#                     cv2.imwrite(save_path, frame)
#                     print(f"✅ [FACE SAVED] Successfully registered {self.register_next_face_as} permanently!")
#                     self.current_person_name = self.register_next_face_as
#                     self.register_next_face_as = None 

#             # --- 3. YOLO OBJECTS & KNOWN FACES ---
#             results = self.model(frame, verbose=False)
#             for result in results:
#                 for box in result.boxes:
#                     conf = float(box.conf[0])
#                     if conf > 0.5:
#                         class_id = int(box.cls[0])
#                         class_name = self.model.names[class_id]
                        
#                         if class_name == 'person' and len(self.known_face_encodings) > 0:
#                             if current_time - self.last_face_check_time > 2.0:
#                                 face_locations = face_recognition.face_locations(rgb_frame)
#                                 face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                                
#                                 temp_name = "person"
#                                 for face_encoding in face_encodings:
#                                     matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
#                                     if True in matches:
#                                         first_match_index = matches.index(True)
#                                         temp_name = self.known_face_names[first_match_index]
                                
#                                 self.current_person_name = temp_name
#                                 self.last_face_check_time = current_time
#                             class_name = self.current_person_name
                        
#                         seen_objects.append({"name": class_name, "confidence": round(conf, 2)})
            
#             # --- 4. SEND CONTEXT TO BRAIN ---
#             if seen_objects and (current_time - self.last_broadcast_time > 1.5):
#                 payload = {
#                     "source": "visual_cortex",
#                     "timestamp": current_time,
#                     "objects": seen_objects
#                 }
#                 self.thalamus.publish("vision_stream", payload)
                
#                 object_names = list(set([obj['name'] for obj in seen_objects])) 
#                 print(f"👁️ [AANKHEIN]: {object_names}")
#                 self.last_broadcast_time = current_time
            
#             annotated_frame = results[0].plot()
#             cv2.imshow("AI Vision - Dynamic Gestures", annotated_frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
                
#         self.cap.release()
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     eyes = VisualCortex()
#     eyes.process_vision()








import cv2
import time
import sys
import os
import easyocr
import face_recognition
import threading
import json
import warnings

# --- WARNING BYPASS ---
warnings.filterwarnings("ignore", category=UserWarning, module="face_recognition")

# --- STANDARD MEDIAPIPE IMPORT ---
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
# --------------------------------

from ultralytics import YOLO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

class VisualCortex:
    def __init__(self):
        self.thalamus = Thalamus()
        print("[VISUAL CORTEX] Loading YOLO model...")
        self.model = YOLO('yolov8n.pt')
        
        print("[VISUAL CORTEX] Loading Text Reader (OCR) on GPU...")
        self.reader = easyocr.Reader(['en'], gpu=True) 
        
        # --- MEDIAPIPE (Hand Tracking Engine) ---
        print("[VISUAL CORTEX] Activating Hand Tracking...")
        self.hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.mp_draw = mp_draw
        self.mp_hands = mp_hands
        # ----------------------------------------------
        
        # --- DYNAMIC FACE MEMORY ---
        self.faces_dir = "memory/faces"
        os.makedirs(self.faces_dir, exist_ok=True)
        self.known_face_encodings = []
        self.known_face_names = []
        self.register_next_face_as = None
        
        print("[VISUAL CORTEX] Recalling known faces from memory...")
        for filename in os.listdir(self.faces_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                img_path = os.path.join(self.faces_dir, filename)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(name)
        print(f"👤 [FACE MEMORY] I remember {len(self.known_face_names)} faces.")
        
        threading.Thread(target=self.listen_for_face_commands, daemon=True).start()
            
        print("[VISUAL CORTEX] Opening laptop camera...")
        self.cap = cv2.VideoCapture(0)
        
        self.last_read_time = 0 
        self.last_broadcast_time = 0
        self.last_face_check_time = 0
        self.last_ocr_time = 0  # NAYA: OCR ko lag free banane ke liye
        self.current_person_name = "person" 

    def listen_for_face_commands(self):
        pubsub = self.thalamus.client.pubsub()
        pubsub.subscribe("face_registration_stream")
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                name_to_save = data.get("name")
                if name_to_save:
                    self.register_next_face_as = name_to_save
                    print(f"\n📸 [FACE CAM] ALERT: Taking a mental snapshot for '{name_to_save}' in the next frame!\n")
        
    def process_vision(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            seen_objects = []
            current_time = time.time()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # --- 1. DYNAMIC HAND GESTURE DETECTION ---
            hand_results = self.hands.process(rgb_frame)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    fingers = []
                    tips = [8, 12, 16, 20]
                    
                    # Thumb
                    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                        
                    # Other 4 fingers
                    for tip in tips:
                        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                            
                    total_fingers = fingers.count(1)
                    gesture_text = f"Hand Gesture: showing {total_fingers} fingers"
                    if total_fingers == 0:
                        gesture_text = "Hand Gesture: Fist (Mutthi band hai)"
                    elif total_fingers == 5:
                        gesture_text = "Hand Gesture: Open Palm (Khula haath)"

                    seen_objects.append({"name": gesture_text, "confidence": 1.0})
            # -----------------------------------------------------------------

            # --- 2. FACE REGISTRATION ---
            if self.register_next_face_as:
                face_locations = face_recognition.face_locations(rgb_frame)
                if face_locations: 
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(self.register_next_face_as)
                    
                    save_path = os.path.join(self.faces_dir, f"{self.register_next_face_as}.jpg")
                    cv2.imwrite(save_path, frame)
                    print(f"✅ [FACE SAVED] Successfully registered {self.register_next_face_as} permanently!")
                    self.current_person_name = self.register_next_face_as
                    self.register_next_face_as = None 

            # --- 3. YOLO OBJECTS, KNOWN FACES & SMART OCR ---
            results = self.model(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:
                        class_id = int(box.cls[0])
                        class_name = self.model.names[class_id]
                        
                        # --- FACE MATCHING ---
                        if class_name == 'person' and len(self.known_face_encodings) > 0:
                            if current_time - self.last_face_check_time > 2.0:
                                face_locations = face_recognition.face_locations(rgb_frame)
                                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                                
                                temp_name = "person"
                                for face_encoding in face_encodings:
                                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
                                    if True in matches:
                                        first_match_index = matches.index(True)
                                        temp_name = self.known_face_names[first_match_index]
                                
                                self.current_person_name = temp_name
                                self.last_face_check_time = current_time
                            class_name = self.current_person_name

                        # --- SMART OCR (Reads Text from Books/Phones without lagging) ---
                        if class_name in ['book', 'cell phone', 'laptop'] and (current_time - self.last_ocr_time > 3.0):
                            try:
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                # Object ko crop karo taaki OCR jaldi padh sake
                                crop = rgb_frame[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
                                if crop.size != 0:
                                    text_results = self.reader.readtext(crop, detail=0)
                                    if text_results:
                                        detected_text = " ".join(text_results)[:50] # Top 50 characters hi lenge
                                        class_name = f"{class_name} (Text written: '{detected_text}')"
                                        print(f"📖 [OCR READ]: {detected_text}")
                                        self.last_ocr_time = current_time
                            except Exception as e:
                                pass
                        
                        seen_objects.append({"name": class_name, "confidence": round(conf, 2)})
            
            # --- 4. SEND CONTEXT TO BRAIN ---
            if seen_objects and (current_time - self.last_broadcast_time > 1.5):
                payload = {
                    "source": "visual_cortex",
                    "timestamp": current_time,
                    "objects": seen_objects
                }
                self.thalamus.publish("vision_stream", payload)
                
                object_names = list(set([obj['name'] for obj in seen_objects])) 
                print(f"👁️ [AANKHEIN]: {object_names}")
                self.last_broadcast_time = current_time
            
            annotated_frame = results[0].plot()
            cv2.imshow("AI Vision - Dynamic & Smart", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    eyes = VisualCortex()
    eyes.process_vision()