import subprocess
import time
import sys
import os

brain_modules = [
    {"name": "Subconscious (Memory)", "path": "subconscious/reflex_engine.py"},
    {"name": "Math Engine (Parietal)", "path": "conscious/math_engine.py"},
    {"name": "Logic Engine (Qwen)", "path": "conscious/logic_engine.py"},
    {"name": "Broca's Area (Voice)", "path": "actors/audio_out.py"},
    {"name": "Ears (Audio Input)", "path": "sensors/audio_in.py"},
    {"name": "Visual Cortex (Eyes)", "path": "sensors/vision_node.py"},
    {"name": "Nexus Interface (UI)", "path": "actors/ui_window.py"}
]

active_processes = []

def wake_up_brain():
    print("🧠 Initiating Nexus AI Brain Sequence (Lightweight Single-Window Mode)...\n")
    
    try:
        for module in brain_modules:
            print(f"⚡ Starting: {module['name']}...")
            
            # Bina naya terminal kholay, sabko isi main terminal me as a background thread chalayega
            process = subprocess.Popen([sys.executable, "-u", module['path']])
            active_processes.append(process)
            
            # 2 second ka gap taaki CPU ekdum se 100% par spike na kare
            time.sleep(2)
            
        print("\n✅ ALL BRAIN LOBES ARE ONLINE!")
        print("🛑 Is window me 'Ctrl + C' dabane se sab ek sath safely band ho jayega.\n")
        print("=" * 60)
        
        # Main script ko zinda rakhne ke liye loop
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 [SHUTDOWN SEQUENCE INITIATED]")
        print("Saare brain modules ko band kiya ja raha hai...")
        for process in active_processes:
            try:
                process.terminate() 
            except:
                pass
        print("🧠 Brain is safely deactivated. Goodbye!")

if __name__ == "__main__":
    if not os.path.exists("sensors/vision_node.py"):
        print("❌ Error: Please run this script from the root of the project folder.")
        sys.exit(1)
        
    wake_up_brain()