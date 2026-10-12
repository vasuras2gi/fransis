import json
import sys
import os
import time
from gtts import gTTS
import pygame

# Project root folder path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

class BrocaArea:
    def __init__(self):
        self.thalamus = Thalamus()
        
        # Pygame mixer initialize karna audio play karne ke liye
        pygame.mixer.init()
        print("🗣️ [BROCA'S AREA] Vocal cords are Online (Using High-Quality Google Voice).", flush=True)

    def speak(self, text):
        try:
            # Text ko mp3 audio file me convert karna
            tts = gTTS(text=text, lang='hi')
            filename = "temp_voice.mp3"
            tts.save(filename)
            
            # Audio play karna
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait jab tak bolna khatam na ho jaye
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Memory clear karna aur temp file delete karna
            pygame.mixer.music.unload()
            if os.path.exists(filename):
                os.remove(filename)
                
        except Exception as e:
            print(f"⚠️ [VOICE ERROR]: {e}")

    def listen_to_thoughts(self):
        pubsub = self.thalamus.client.pubsub()
        pubsub.subscribe("speech_stream")
        print("🔊 [BROCA'S AREA] Listening for conscious thoughts...", flush=True)
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                # Bytes ko string me decode karna
                channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else message['channel']
                data = json.loads(message['data'])
                text_to_speak = data.get("text")
                
                if text_to_speak:
                    # Special symbols ko saaf karke bolna
                    clean_text = text_to_speak.replace("*", "").replace("#", "")
                    self.speak(clean_text)

if __name__ == "__main__":
    vocal_cords = BrocaArea()
    vocal_cords.listen_to_thoughts()



# import json
# import sys
# import os
# import pyttsx3

# # Project root folder path me add karna
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from memory.redis_broker import Thalamus

# class BrocaArea:
#     def __init__(self):
#         self.thalamus = Thalamus()
#         self.engine = pyttsx3.init()
        
#         # Awaaz aur speed set karna
#         voices = self.engine.getProperty('voices')
#         # voices[0] normally male voice hoti hai, voices[1] female hoti hai
#         self.engine.setProperty('voice', voices[0].id) 
#         self.engine.setProperty('rate', 160) # Bolne ki speed
        
#         print("🗣️ [BROCA'S AREA] Vocal cords are Online. Ready to speak.")

#     def listen_to_thoughts(self):
#         pubsub = self.thalamus.subscribe("speech_stream")
#         print("🔊 [BROCA'S AREA] Listening for conscious thoughts to broadcast...")
        
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 data = json.loads(message['data'])
#                 text_to_speak = data.get("text")
                
#                 if text_to_speak:
#                     # Special characters hata dete hain taaki smooth bole
#                     clean_text = text_to_speak.replace("*", "").replace("#", "")
#                     self.engine.say(clean_text)
#                     self.engine.runAndWait()

# if __name__ == "__main__":
#     vocal_cords = BrocaArea()
#     vocal_cords.listen_to_thoughts()