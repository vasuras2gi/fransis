import json
import time
import chromadb
import sys
import os

# Project root folder path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

class ReflexEngine:
    def __init__(self):
        self.thalamus = Thalamus()
        print("🧠 [SUBCONSCIOUS] Waking up...")
        
        # Persistent memory - ye folder ban jayega project me taaki restart par memory na ude
        self.chroma_client = chromadb.PersistentClient(path="./memory/vector_store")
        
        # Collection (Memory box)
        self.collection = self.chroma_client.get_or_create_collection(name="visual_memory")
        print("🧠 [SUBCONSCIOUS] Vector Memory loaded. Ready to learn.")

    def process_vision_stream(self):
        pubsub = self.thalamus.subscribe("vision_stream")
        print("🧠 [SUBCONSCIOUS] Listening to Visual Cortex (Eyes)...")
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                objects = data.get('objects', [])
                
                # Ek dictionary banayenge taaki ek frame me duplicate na aaye
                unique_objects = {obj['name'] for obj in objects}
                
                for name in unique_objects:
                    # Memory me check karo ki kya pehle dekha hai?
                    results = self.collection.query(
                        query_texts=[name],
                        n_results=1
                    )
                    
                    # ChromaDB distance return karta hai. Distance kam matlab similar/familiar.
                    # Agar list khali nahi hai aur distance threshold se kam hai:
                    if results['distances'] and len(results['distances'][0]) > 0 and results['distances'][0][0] < 1.0:
                        # Pehle dekha hua hai, Reflex action trigger
                        print(f"⚡ [REFLEX] '{name}' already in memory. Ignoring to save compute.")
                    else:
                        # Naya object hai!
                        print(f"🚨 [ALERT] '{name}' is completely NEW! Saving to memory and waking up Conscious Mind!")
                        
                        # Memory me permanently save kar lo
                        self.collection.add(
                            documents=[name],
                            metadatas=[{"first_seen": time.time(), "type": "visual_object"}],
                            ids=[f"{name}_{int(time.time())}"]
                        )
                        
                        # Conscious mind ko jagao aur deep analysis ke liye bhejo (Ye hum aage banayenge)
                        self.thalamus.publish("conscious_trigger", {"task": "analyze_new_object", "object": name})

if __name__ == "__main__":
    subconscious = ReflexEngine()
    subconscious.process_vision_stream()



    
# import json
# import time
# import chromadb
# import sys
# import os

# # Project root folder path me add karna
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from memory.redis_broker import Thalamus

# class ReflexEngine:
#     def __init__(self):
#         self.thalamus = Thalamus()
#         print("🧠 [SUBCONSCIOUS] Waking up...")
        
#         # Persistent memory - ye folder ban jayega project me taaki restart par memory na ude
#         self.chroma_client = chromadb.PersistentClient(path="./memory/vector_store")
        
#         # Collection (Memory box)
#         self.collection = self.chroma_client.get_or_create_collection(name="visual_memory")
#         print("🧠 [SUBCONSCIOUS] Vector Memory loaded. Ready to learn.")

#     def process_vision_stream(self):
#         pubsub = self.thalamus.subscribe("vision_stream")
#         print("🧠 [SUBCONSCIOUS] Listening to Visual Cortex (Eyes)...")
        
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 data = json.loads(message['data'])
#                 objects = data.get('objects', [])
                
#                 # Ek dictionary banayenge taaki ek frame me duplicate na aaye
#                 unique_objects = {obj['name'] for obj in objects}
                
#                 for name in unique_objects:
#                     # Memory me check karo ki kya pehle dekha hai?
#                     results = self.collection.query(
#                         query_texts=[name],
#                         n_results=1
#                     )
                    
#                     # ChromaDB distance return karta hai. Distance kam matlab similar/familiar.
#                     # Agar list khali nahi hai aur distance threshold se kam hai:
#                     if results['distances'] and len(results['distances'][0]) > 0 and results['distances'][0][0] < 1.0:
#                         # Pehle dekha hua hai, Reflex action trigger
#                         print(f"⚡ [REFLEX] '{name}' already in memory. Ignoring to save compute.")
#                     else:
#                         # Naya object hai!
#                         print(f"🚨 [ALERT] '{name}' is completely NEW! Saving to memory and waking up Conscious Mind!")
                        
#                         # Memory me permanently save kar lo
#                         self.collection.add(
#                             documents=[name],
#                             metadatas=[{"first_seen": time.time(), "type": "visual_object"}],
#                             ids=[f"{name}_{int(time.time())}"]
#                         )
                        
#                         # Conscious mind ko jagao aur deep analysis ke liye bhejo (Ye hum aage banayenge)
#                         self.thalamus.publish("conscious_trigger", {"task": "analyze_new_object", "object": name})

# if __name__ == "__main__":
#     subconscious = ReflexEngine()
#     subconscious.process_vision_stream()