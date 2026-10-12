import json
import sys
import os
import time
import sympy as sp

# Project root folder path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

class ParietalLobe:
    def __init__(self):
        self.thalamus = Thalamus()
        print("📐 [MATH ENGINE] Parietal Lobe is Online. Viewing the world in equations.")
        
    def calculate_physics(self, object_name):
        """Object ke hisaab se uska fundamental physics law aur equation nikalna"""
        print(f"\n🔢 [CALCULATING] Applying mathematics to '{object_name}'...")
        
        # SymPy variables
        m, v, r, t, g, h, F, E, c = sp.symbols('m v r t g h F E c')
        
        # Object ke basis par logic (Hum isme aage aur rules add kar sakte hain)
        if "book" in object_name.lower():
            law = "Potential Energy (Gravity)"
            eq = sp.Eq(E, m * g * h)
            explanation = "If this book falls, its potential energy converts to kinetic energy."
        
        elif "cell phone" in object_name.lower() or "laptop" in object_name.lower():
            law = "Ohm's Law & Power (Electronics)"
            I, R, P = sp.symbols('I R P')
            eq = sp.Eq(P, (I**2) * R)
            explanation = "This device operates on electrical power dissipated as heat and light."
            
        elif "person" in object_name.lower():
            law = "Biomechanics (Work & Energy)"
            W, d = sp.symbols('W d')
            eq = sp.Eq(W, F * d)
            explanation = "Human movement requires metabolic energy converted into mechanical work."
            
        else:
            law = "Newton's Second Law of Motion"
            eq = sp.Eq(F, m * (v / t))
            explanation = "Any change in this object's state requires an external force."
            
        # Format the mathematical thought
        math_thought = f"From a physics perspective, the '{object_name}' is governed by {law}. The equation is {eq}. {explanation}"
        print(f"⚛️ [PHYSICS RESULT]: {math_thought}")
        return math_thought

    def listen_for_objects(self):
        # Ye Subconscious se directly signal lega
        pubsub = self.thalamus.subscribe("conscious_trigger")
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data.get("task") == "analyze_new_object":
                    obj_name = data.get("object")
                    
                    # Math calculate karo
                    math_perspective = self.calculate_physics(obj_name)
                    
                    # Is mathematical thought ko hum wapas Thalamus me bhejenge
                    # Taaki LLM (Qwen) is equation ko padh kar apna answer banaye
                    self.thalamus.publish("math_stream", {"object": obj_name, "math_thought": math_perspective})
                    time.sleep(2)

if __name__ == "__main__":
    math_brain = ParietalLobe()
    math_brain.listen_for_objects()