import json
from memory.redis_broker import Thalamus

def listen_to_brain():
    brain = Thalamus()
    print("[MAIN BRAIN] Listening to all sensory inputs...")
    
    # Vision stream subscribe kar rahe hain
    pubsub = brain.subscribe("vision_stream")
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            # Ek second me multiple frames aayenge, hum list print karte hain
            print(f"👉 [SUBCONSCIOUS RECEIVED]: {len(data['objects'])} objects detected.")

if __name__ == "__main__":
    listen_to_brain()