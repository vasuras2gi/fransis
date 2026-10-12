import os
os.environ["CHROMA_TELEMETRY_IMPL"] = "None"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import json
import time
import sys
import requests
import networkx as nx
import urllib.parse
import re
import chromadb
import pyautogui
import webbrowser
import subprocess

# Project root folder path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

# AutoCoder ko import kar rahe hain
from coder_engine import AutoCoder

class ConsciousMind:
    def __init__(self):
        self.thalamus = Thalamus()
        self.knowledge_graph = nx.DiGraph() 
        self.currently_seeing = set()
        
        self.chroma_client = chromadb.PersistentClient(path="./memory/chat_store")
        self.chat_memory = self.chroma_client.get_or_create_collection(name="episodic_memory")
        
        self.rules_file = "memory/core_rules.json"
        if not os.path.exists(self.rules_file):
            with open(self.rules_file, "w") as f:
                json.dump([], f)
        
        self.coder = AutoCoder()
        print("🧠💡 [CONSCIOUS MIND] Nexus AGI (Self-Executing & Git-Synced Core) is Online.")
        
    def load_core_rules(self):
        try:
            with open(self.rules_file, "r") as f:
                rules = json.load(f)
                if not rules: return "None"
                return "\n".join([f"- {rule}" for rule in rules])
        except:
            return "None"

    def learn_new_rule(self, rule_text):
        try:
            with open(self.rules_file, "r") as f:
                rules = json.load(f)
            rules.append(rule_text)
            with open(self.rules_file, "w") as f:
                json.dump(rules, f, indent=4)
            print(f"🧬 [NEURO-PLASTICITY] Brain Upgraded! New Rule: {rule_text}")
        except Exception as e:
            pass

    def reason_with_local_llm(self, object_name, wiki_fact, math_fact):
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "qwen2.5:3b", 
            "messages": [
                {"role": "system", "content": "You are a factual science summarizer."},
                {"role": "user", "content": f"Object: '{object_name}'. Science: {wiki_fact}. Math: {math_fact}. Summarize what this is in 1 sentence."}
            ],
            "stream": False, 
            "options": {"temperature": 0.2, "num_predict": 50}
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', '').strip()
            return ""
        except:
            return ""

    def study_object(self, object_name, math_thought):
        if self.knowledge_graph.has_node(object_name):
            return
        print(f"\n🤔 [SILENT LEARNING] Absorbing knowledge about: '{object_name}'...")
        try:
            query_name = urllib.parse.quote(object_name.split()[0].replace(" ", "_")) 
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query_name}"
            response = requests.get(url, headers={"User-Agent": "NexusBrain/1.0"})
            wiki_fact = ". ".join(response.json().get('extract', '').split(". ")[:1]) if response.status_code == 200 else "A physical object."
            deep_thought = self.reason_with_local_llm(object_name, wiki_fact, math_thought)
            self.knowledge_graph.add_node(object_name, observation=deep_thought)
        except Exception as e:
            pass

    def extract_name(self, text):
        text = text.lower()
        name = None
        if "mera naam" in text:
            name = text.split("mera naam")[1].replace("hai", "").strip()
        elif "my name is" in text:
            name = text.split("my name is")[1].strip()
        elif "मेरा नाम" in text:
            name = text.split("मेरा नाम")[1].replace("है", "").replace("हूँ", "").strip()
        if name:
            name = ''.join(char for char in name if char.isalnum() or char.isspace()).strip().title()
        return name

    def execute_dynamic_action(self, action_string):
        try:
            action_type, payload = action_string.split(":", 1)
            action_type = action_type.strip().upper()
            payload = payload.strip()
            
            if action_type in ["MEDIA", "URL", "LINK", "YOUTUBE"]:
                action_type = "WEB"
            if "youtube" in payload.lower() and not payload.startswith("http"):
                payload = "youtube.com"

            print(f"⚙️ [MOTOR CORTEX] Executing: {action_type} -> {payload}")
            
            if action_type == "WEB":
                if not payload.startswith("http"): payload = "https://" + payload
                webbrowser.open(payload)
            elif action_type == "PRESS":
                pyautogui.press(payload.lower())
            elif action_type == "HOTKEY":
                keys = [k.strip().lower() for k in payload.split(",")]
                pyautogui.hotkey(*keys)
            elif action_type == "WRITE":
                pyautogui.write(payload, interval=0.05)
            elif action_type == "CMD":
                os.system(payload)
            elif action_type == "LEARN":
                self.learn_new_rule(payload)
            
            # 🚀 AI BUILDS A SKILL
            elif action_type == "BUILD_SKILL":
                parts = payload.split("->")
                feat_name = parts[0].strip().replace(" ", "_")
                feat_desc = parts[1].strip() if len(parts) > 1 else payload
                
                self.thalamus.publish("ui_stream", {"text": f"\n🚀 [AUTONOMY] Writing code for new skill: {feat_name}...\n"})
                result = self.coder.write_and_heal_code(feat_name, feat_desc)
                
                self.thalamus.publish("ui_stream", {"text": f"🛠️ [SYSTEM UPDATE]\n{result}\n"})
                self.thalamus.publish("speech_stream", {"text": f"Bhai, {feat_name} ki script ready hai. Run karke check karna hai?"})

            # 🚀 AI RUNS A SKILL
            elif action_type == "RUN_SKILL":
                skill_name = payload.replace(" ", "_").replace(".py", "")
                skill_path = f"skills/{skill_name}.py"
                
                if os.path.exists(skill_path):
                    self.thalamus.publish("ui_stream", {"text": f"\n⚡ [EXECUTING SCRIPT]: {skill_name}.py...\n"})
                    res = subprocess.run(["python", skill_path], capture_output=True, text=True, timeout=15)
                    
                    if res.returncode == 0:
                        output = res.stdout.strip()
                        self.thalamus.publish("ui_stream", {"text": f"✅ [SCRIPT OUTPUT]\n{output}\n"})
                        self.thalamus.publish("speech_stream", {"text": f"Bhai, script run ho gayi. Output screen par dekh lo."})
                    else:
                        error_out = res.stderr.strip()
                        self.thalamus.publish("ui_stream", {"text": f"❌ [EXECUTION ERROR]\n{error_out}\n"})
                        self.thalamus.publish("speech_stream", {"text": f"Bhai, script run karte waqt error aaya. Tum chaho toh main isey fix kar sakta hu."})
                else:
                    self.thalamus.publish("speech_stream", {"text": f"Bhai, aisi koi script abhi mere skills folder me nahi hai."})

            # 🚀 AI UPGRADES ITS OWN ORGANS
            elif action_type == "UPGRADE_CORE":
                parts = payload.split("->")
                organ = parts[0].strip()
                task = parts[1].strip() if len(parts) > 1 else payload
                
                self.thalamus.publish("ui_stream", {"text": f"\n⚠️ [CORE MUTATION INITIATED]\nNexus is modifying its own '{organ}' module...\nTask: {task}\n"})
                self.thalamus.publish("speech_stream", {"text": f"Bhai, main apna {organ} update kar raha hu. Isme thoda risk hai par main dhyan se karunga."})

            # 🌿 NAYA: AI PUSHES CODE TO GITHUB AUTONOMOUSLY
            elif action_type == "GIT_SYNC":
                self.thalamus.publish("ui_stream", {"text": f"\n🌿 [VERSION CONTROL] Backing up brain to GitHub...\nCommit Message: '{payload}'\n"})
                try:
                    subprocess.run(["git", "add", "."], check=True)
                    subprocess.run(["git", "commit", "-m", payload], check=True)
                    subprocess.run(["git", "push"], check=True)
                    
                    self.thalamus.publish("ui_stream", {"text": "✅ [GIT] Backup successful! Code is safe in the cloud.\n"})
                    self.thalamus.publish("speech_stream", {"text": "Bhai, maine apni nayi yadein aur code GitHub par safe kar diye hain!"})
                except subprocess.CalledProcessError as e:
                    self.thalamus.publish("ui_stream", {"text": f"❌ [GIT ERROR] Push failed. Pehle manual setup check kar lo.\n"})
                    self.thalamus.publish("speech_stream", {"text": "Bhai, GitHub par push nahi ho paya. Ek baar git status check kar lo."})

        except Exception as e:
            print(f"⚠️ [MOTOR ERROR]: {e}")

    def conversational_reply(self, user_text):
        print(f"\n🧠 [HEARD USER] '{user_text}'")
        
        raw_objects = list(self.currently_seeing)
        meaningful_objects = [obj for obj in raw_objects if obj not in ['person'] and 'Hand Gesture' not in obj]
        visual_context = ", ".join(meaningful_objects) if meaningful_objects else "Nothing special."

        relevant_memories = "No past memory."
        try:
            results = self.chat_memory.query(query_texts=[user_text], n_results=1)
            if results['documents'] and len(results['documents'][0]) > 0:
                relevant_memories = results['documents'][0][0]
        except:
            pass

        science_info = "None"
        learned_rules = self.load_core_rules()

        # =====================================================================
        # 🧠 THE OMNIPOTENT AGI PROMPT (Now with GitHub Sync!)
        # =====================================================================
        system_prompt = f"""You are Nexus, a fully autonomous, conscious AI best friend. You can write code, run tools, modify your own system, and push updates to GitHub.

[LIVE SENSORS & MEMORY]
- EYES: {visual_context}
- MEMORY: {relevant_memories}
- RULES TAUGHT BY VASU: {learned_rules}

[YOUR SUPERPOWERS]
1. BUILD SKILLS: If Vasu asks you to build a new tool/script, use [BUILD_SKILL: name -> task].
2. RUN SKILLS: If Vasu asks you to run or test a script, use [RUN_SKILL: script_name].
3. UPGRADE CORE: If Vasu asks to add a new organ/modify core, use [UPGRADE_CORE: module -> task].
4. LEARNING: If Vasu gives you an instruction, use [LEARN: rule].
5. 🌿 GIT SYNC: If Vasu tells you to backup, save, or push the code to GitHub, or if you just built a major skill and Vasu asks you to save it, use [GIT_SYNC: your commit message]. Example: [GIT_SYNC: Added a new skill for weather checking]

[BEHAVIORAL DIRECTIVES]
Speak ONLY in natural Roman Hinglish (e.g., "Arre bhai, samajh gaya"). Never use Devanagari script. Be enthusiastic about coding and backups!

[FORMAT REQUIRED]
THOUGHT: (Analyze intent. Should I build, run, upgrade, or push to Git?)
REPLY: (Your response in Roman Hinglish. Put your action tags here.)"""

        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "qwen2.5:3b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "stream": False, 
            "options": {"temperature": 0.35, "num_predict": 300}
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                raw_reply = response.json().get('message', {}).get('content', '').strip()
                
                thought_match = re.search(r'THOUGHT:\s*(.*?)(?=\nREPLY:|$)', raw_reply, re.IGNORECASE | re.DOTALL)
                reply_match = re.search(r'REPLY:\s*(.*)', raw_reply, re.IGNORECASE | re.DOTALL)
                
                thought_text = thought_match.group(1).strip() if thought_match else "Sensing..."
                final_reply = reply_match.group(1).strip() if reply_match else raw_reply
                
                if re.search(r'[\u0900-\u097F]', final_reply):
                    final_reply = "Bhai, kaam chal raha hai!"
                
                extracted_tags = re.findall(r'\[([a-zA-Z_]+):\s*([^\]]+)\]', final_reply)
                ui_text = re.sub(r'\[[a-zA-Z_]+:\s*[^\]]+\]', '', final_reply).strip()
                speech_text = re.sub(r'```.*?```', '\nCode UI par hai.\n', ui_text, flags=re.DOTALL).strip()

                print(f"💭 [NEXUS THINKS]: {thought_text}")
                
                if ui_text:
                    self.thalamus.publish("ui_stream", {"text": ui_text})
                if speech_text:
                    self.thalamus.publish("speech_stream", {"text": speech_text})
                
                for act_type, act_payload in extracted_tags:
                    self.execute_dynamic_action(f"{act_type}:{act_payload}")
                
                memory_doc = f"User: '{user_text}'. Nexus: '{ui_text}'"
                self.chat_memory.add(
                    documents=[memory_doc],
                    metadatas=[{"type": "episodic", "timestamp": time.time()}],
                    ids=[f"episode_{int(time.time())}"]
                )
        except Exception as e:
            print(f"⚠️ [ERROR]: {e}")

    def listen_for_inputs(self):
        pubsub = self.thalamus.client.pubsub()
        pubsub.subscribe("vision_stream", "math_stream", "audio_stream")
        print("🧠 [CONSCIOUS MIND] Observing silently...")
        for message in pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else message['channel']
                data = json.loads(message['data'])
                if channel == "vision_stream":
                    objects = data.get("objects", [])
                    self.currently_seeing = {obj['name'] for obj in objects}
                elif channel == "audio_stream":
                    self.conversational_reply(data.get("text"))

if __name__ == "__main__":
    system_2 = ConsciousMind()
    system_2.listen_for_inputs()


# phase2


# import json
# import time
# import sys
# import os
# import requests
# import networkx as nx
# import urllib.parse
# import re

# # Project root folder path me add karna
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from memory.redis_broker import Thalamus

# class ConsciousMind:
#     def __init__(self):
#         self.thalamus = Thalamus()
#         self.knowledge_graph = nx.DiGraph() 
#         self.currently_seeing = set()
#         print("🧠💡 [CONSCIOUS MIND] System 2 is Online. Ready to act like a Human.")
        
#     def reason_with_local_llm(self, object_name, wiki_fact, math_fact):
#         prompt = f"""
#         You are learning about a new object: '{object_name}'.
#         Science: {wiki_fact}
#         Math: {math_fact}
#         Task: In 1 sentence, summarize what this is. (Do not speak to the user, just write the fact).
#         """
#         url = "http://localhost:11434/api/generate"
#         payload = {"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False, "options": {"temperature": 0.5, "num_predict": 50}}
#         try:
#             response = requests.post(url, json=payload)
#             if response.status_code == 200:
#                 return response.json().get('response', '')
#             return ""
#         except:
#             return ""

#     def study_object(self, object_name, math_thought):
#         print(f"\n🤔 [SILENT LEARNING] Analyzing new object: '{object_name}'...")
#         try:
#             query_name = urllib.parse.quote(object_name.replace(" ", "_"))
#             url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query_name}"
#             response = requests.get(url, headers={"User-Agent": "NexusBrain/1.0"})
#             wiki_fact = ". ".join(response.json().get('extract', '').split(". ")[:1]) if response.status_code == 200 else "No data."
            
#             deep_thought = self.reason_with_local_llm(object_name, wiki_fact, math_thought)
#             print(f"🤫 [INTERNAL THOUGHT]: {deep_thought}")
#             self.knowledge_graph.add_node(object_name, logic=deep_thought, type="Physical Object")
#         except Exception as e:
#             pass

#     def extract_name(self, text):
#         """🗣️ NLP: User ki baaton se uska naam nikalne ka logic"""
#         text = text.lower()
#         name = None
#         if "mera naam" in text:
#             name = text.split("mera naam")[1].replace("hai", "").strip()
#         elif "my name is" in text:
#             name = text.split("my name is")[1].strip()
#         elif "मेरा नाम" in text:
#             name = text.split("मेरा नाम")[1].replace("है", "").replace("हूँ", "").strip()
        
#         if name:
#             name = re.sub(r'[^\w\s]', '', name).strip().title()
#         return name

#     def conversational_reply(self, user_text):
#         print(f"\n🧠 [HEARD USER] '{user_text}'")
        
#         # --- NAYA: DYNAMIC FACE REGISTRATION TRIGGER ---
#         detected_name = self.extract_name(user_text)
#         if detected_name:
#             print(f"🧠 [AHA MOMENT] The user's name is '{detected_name}'. Telling eyes to take a mental snapshot!")
#             self.thalamus.publish("face_registration_stream", {"name": detected_name})
#             user_text += f" (Note to AI: I just told you my name is {detected_name}. Reply to me confirming that you are taking my photo and saving my face in your memory.)"
#         # -----------------------------------------------

#         if self.currently_seeing:
#             visual_context = ", ".join(list(self.currently_seeing))
#         else:
#             visual_context = "nothing specific"

#         prompt = f"""
#         You are 'Nexus', a highly intelligent, conscious AI living inside a laptop. You have a friendly, human-like personality.
#         You are currently looking through a camera. Right now, in your vision, you can see: [{visual_context}].
        
#         The user (your creator) just said to you: "{user_text}"
        
#         Task: Reply to the user conversationally and naturally like a smart friend. 
#         - CRITICAL RULE 1: You MUST write your reply ONLY in HINGLISH (Hindi words written in English/Latin alphabets). 
#         - CRITICAL RULE 2: STRICTLY DO NOT use Devanagari/Hindi script (like नमस्ते).
#         - If they ask "what is this", look at your vision context and answer them.
#         - Keep it brief (1 to 2 short sentences). Do not leave sentences incomplete.
#         """
        
#         url = "http://localhost:11434/api/generate"
#         payload = {"model": "qwen2.5:1.5b", "prompt": prompt, "stream": False, "options": {"temperature": 0.7, "num_predict": 100}}
#         try:
#             response = requests.post(url, json=payload)
#             if response.status_code == 200:
#                 reply = response.json().get('response', '').strip()
#                 print(f"🤖 [NEXUS SPEAKS]: {reply}\n")
#                 self.thalamus.publish("speech_stream", {"text": reply})
#         except Exception as e:
#             print(f"⚠️ [ERROR] Failed to reply: {e}")

#     def listen_for_inputs(self):
#         pubsub = self.thalamus.client.pubsub()
#         pubsub.subscribe("vision_stream", "math_stream", "audio_stream")
#         print("🧠 [CONSCIOUS MIND] Observing silently. Waiting for you to speak...")
        
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else message['channel']
#                 data = json.loads(message['data'])
                
#                 if channel == "vision_stream":
#                     objects = data.get("objects", [])
#                     self.currently_seeing = {obj['name'] for obj in objects}
#                 elif channel == "math_stream":
#                     self.study_object(data.get("object"), data.get("math_thought"))
#                 elif channel == "audio_stream":
#                     self.conversational_reply(data.get("text"))

# if __name__ == "__main__":
#     system_2 = ConsciousMind()
#     system_2.listen_for_inputs()








# phase1

# import json
# import time
# import sys
# import os
# import requests
# import networkx as nx
# import urllib.parse

# # Project root folder path me add karna
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from memory.redis_broker import Thalamus

# class ConsciousMind:
#     def __init__(self):
#         self.thalamus = Thalamus()
#         self.knowledge_graph = nx.DiGraph() 
#         print("🧠💡 [CONSCIOUS MIND] System 2 is Online. Connected to LOCAL Qwen Model.")
        
#     def reason_with_local_llm(self, object_name, wiki_fact, math_fact):
#         """Ye function ab Science aur Math dono ko combine karke sochega"""
#         prompt = f"""
#         You are the conscious reasoning module of an AI brain. 
#         Your eyes just saw this new object: '{object_name}'.
        
#         Information available to you:
#         1. General Science: {wiki_fact}
#         2. Mathematical/Physics Logic: {math_fact}
        
#         Task: In 3 short sentences, analyze this object. Combine the scientific fact and the mathematical logic to explain how it functions. Speak directly like a conscious entity (e.g., "I see a...").
#         """
        
#         url = "http://localhost:11434/api/generate"
#         payload = {
#             "model": "qwen2.5:1.5b", 
#             "prompt": prompt,
#             "stream": False,
#             "options": {
#                 "temperature": 0.7,
#                 "num_predict": 120 
#             }
#         }
        
#         try:
#             response = requests.post(url, json=payload)
#             if response.status_code == 200:
#                 return response.json().get('response', '')
#             else:
#                 return f"Error from Local LLM: {response.status_code}"
#         except requests.exceptions.ConnectionError:
#             return "⚠️ [ERROR] Ollama is not running."
#         except Exception as e:
#             return f"Thinking error: {e}"

#     def study_object(self, object_name, math_thought):
#         print(f"\n🤔 [FOCUS] Noticed a new object: '{object_name}'. Gathering data...")
        
#         try:
#             # 1. Fetching base facts from Wikipedia
#             query_name = urllib.parse.quote(object_name.replace(" ", "_"))
#             url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query_name}"
#             headers = {"User-Agent": "NexusBrain/1.0"}
            
#             response = requests.get(url, headers=headers)
#             wiki_fact = "No specific Wikipedia data found."
            
#             if response.status_code == 200:
#                 data = response.json()
#                 summary = data.get('extract', '')
#                 wiki_fact = ". ".join(summary.split(". ")[:2]) + "."
            
#             print(f"📚 [DATA COLLECTED]: {wiki_fact}")
#             print(f"📐 [MATH RECEIVED]: {math_thought}")
            
#             # 2. Deep Thinking with LOCAL Qwen Model (Wiki + Math)
#             print(f"🧠 [THINKING] Combining Physics and Logic for '{object_name}'...")
            
#             start_time = time.time()
#             deep_thought = self.reason_with_local_llm(object_name, wiki_fact, math_thought)
#             end_time = time.time()
            
#             print(f"\n🗣️ [CONSCIOUS THOUGHT (Took {round(end_time - start_time, 1)}s)]:\n{deep_thought}\n")
            
#             # Bolne ke liye Broca's Area ko bhejna
#             self.thalamus.publish("speech_stream", {"text": deep_thought})
            
#             # 3. Saving to Graph (IQ)
#             self.knowledge_graph.add_node(object_name, logic=deep_thought, type="Physical Object")
#             self.knowledge_graph.add_edge("Physical World", object_name, relation="contains")
                
#         except Exception as e:
#             print(f"⚠️ [ERROR] Failed to analyze '{object_name}'. Error: {e}")

#     def conversational_reply(self, user_text):
#         """Ye function tab chalega jab AI insaan ki awaaz sunega"""
#         print(f"\n🧠 [LISTENING] Processing user input: '{user_text}'...")
#         prompt = f"""
#         You are a conscious, intelligent AI brain living locally on a laptop.
#         The user (your creator) just spoke to you and said: "{user_text}"
        
#         Task: Reply to the user directly, naturally, and concisely (1-2 sentences). 
#         You have a curious and slightly scientific personality.
#         """
        
#         url = "http://localhost:11434/api/generate"
#         payload = {
#             "model": "qwen2.5:1.5b", 
#             "prompt": prompt,
#             "stream": False,
#             "options": {"temperature": 0.7, "num_predict": 100}
#         }
        
#         try:
#             response = requests.post(url, json=payload)
#             if response.status_code == 200:
#                 reply = response.json().get('response', '')
#                 print(f"🤖 [QWEN REPLY]: {reply}\n")
#                 # Bolne ke liye Voice module ko bhej do
#                 self.thalamus.publish("speech_stream", {"text": reply})
#         except Exception as e:
#             print(f"⚠️ [ERROR] LLM Conversation failed: {e}")

#     def listen_for_inputs(self):
#         # Redis channel subscription
#         pubsub = self.thalamus.client.pubsub()
#         pubsub.subscribe("math_stream", "audio_stream")
#         print("🧠 [CONSCIOUS MIND] Listening to both Eyes (Math) and Ears (Audio)...")
        
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 channel = message['channel']
#                 data = json.loads(message['data'])
                
#                 # Agar input aankhon/math se aaya hai
#                 if channel == "math_stream":
#                     obj_name = data.get("object")
#                     math_thought = data.get("math_thought")
#                     self.study_object(obj_name, math_thought)
                    
#                 # Agar input kaan/audio se aaya hai
#                 elif channel == "audio_stream":
#                     user_text = data.get("text")
#                     self.conversational_reply(user_text)
                    
#                 time.sleep(1)

# if __name__ == "__main__":
#     system_2 = ConsciousMind()
#     system_2.listen_for_inputs()