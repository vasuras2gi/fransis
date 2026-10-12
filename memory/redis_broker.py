import redis
import json

class Thalamus:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            # Redis server se connect kar rahe hain
            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.client.ping()
            print("[THALAMUS] Connected to Redis. Brain is online.")
        except redis.ConnectionError:
            print("[ERROR] Redis server is not running!")

    def publish(self, channel, data):
        """Kisi bhi brain part se data bhejne ke liye"""
        message = json.dumps(data)
        self.client.publish(channel, message)
        # Short-term working memory me state save karne ke liye
        self.client.set(f"current_state:{channel}", message, ex=300) # 5 min expiry

    def subscribe(self, channel):
        """Kisi channel ko continuously sunne ke liye"""
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub

# Test karne ke liye
if __name__ == "__main__":
    brain_router = Thalamus()
    brain_router.publish("vision_stream", {"object": "setup_complete", "status": "ready"})