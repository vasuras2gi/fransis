import json
import time
import sys
import os
import speech_recognition as sr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

class Ears:
    def __init__(self):
        self.thalamus = Thalamus()
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 400  # Default noise level
        print("👂 [EARS ONLINE] Microphone activating...", flush=True)

    def start_listening(self):
        try:
            with sr.Microphone() as source:
                print("🎙️ [MIC CALIBRATING] Adjusting for noise (2 seconds)...", flush=True)
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("\n✅ [MIC READY] BOLO! (Listening for your voice...)\n", flush=True)
                
                while True:
                    try:
                        # timeout=5 ka matlab agar 5 second tak koi nahi bola, toh stuck nahi hoga, wapas sunega
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
                        # language="hi-IN" lagane se ye Hindi/Hinglish bohot clear pakdega
                        text = self.recognizer.recognize_google(audio, language="hi-IN")
                        print(f"\n🗣️ [USER SAID]: {text}", flush=True)
                        
                        self.thalamus.publish("audio_stream", {"text": text})
                        
                    except sr.WaitTimeoutError:
                        # Koi kuch nahi bola, background me chalta rahega
                        pass
                    except sr.UnknownValueError:
                        # Awaaz aayi par samajh nahi aayi
                        pass
                    except Exception as e:
                        print(f"⚠️ [MIC PROCESS ERROR]: {e}", flush=True)
                        
        except Exception as e:
            print(f"\n❌ [CRITICAL ERROR] Mic open nahi ho raha! Error: {e}", flush=True)
            print("Check karo ki PyAudio installed hai ya Windows me Python ko Mic ki permission hai ya nahi.\n", flush=True)

if __name__ == "__main__":
    ears = Ears()
    ears.start_listening()



# import json
# import time
# import sys
# import os
# import speech_recognition as sr

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from memory.redis_broker import Thalamus

# class Ears:
#     def __init__(self):
#         self.thalamus = Thalamus()
#         self.recognizer = sr.Recognizer()
#         self.recognizer.dynamic_energy_threshold = True
#         self.recognizer.energy_threshold = 400  # Default noise level
#         print("👂 [EARS ONLINE] Microphone activating...", flush=True)

#     def start_listening(self):
#         try:
#             with sr.Microphone() as source:
#                 print("🎙️ [MIC CALIBRATING] Adjusting for noise (2 seconds)...", flush=True)
#                 self.recognizer.adjust_for_ambient_noise(source, duration=2)
#                 print("\n✅ [MIC READY] BOLO! (Listening for your voice...)\n", flush=True)
                
#                 while True:
#                     try:
#                         # timeout=5 ka matlab agar 5 second tak koi nahi bola, toh stuck nahi hoga, wapas sunega
#                         audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
#                         # language="hi-IN" lagane se ye Hindi/Hinglish bohot clear pakdega
#                         text = self.recognizer.recognize_google(audio, language="hi-IN")
#                         print(f"\n🗣️ [USER SAID]: {text}", flush=True)
                        
#                         self.thalamus.publish("audio_stream", {"text": text})
                        
#                     except sr.WaitTimeoutError:
#                         # Koi kuch nahi bola, background me chalta rahega
#                         pass
#                     except sr.UnknownValueError:
#                         # Awaaz aayi par samajh nahi aayi
#                         pass
#                     except Exception as e:
#                         print(f"⚠️ [MIC PROCESS ERROR]: {e}", flush=True)
                        
#         except Exception as e:
#             print(f"\n❌ [CRITICAL ERROR] Mic open nahi ho raha! Error: {e}", flush=True)
#             print("Check karo ki PyAudio installed hai ya Windows me Python ko Mic ki permission hai ya nahi.\n", flush=True)

# if __name__ == "__main__":
#     ears = Ears()
#     ears.start_listening()