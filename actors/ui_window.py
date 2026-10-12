import tkinter as tk
from tkinter import scrolledtext
import redis
import json
import threading
import sys
import os

# Project root folder path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.redis_broker import Thalamus

class NexusUI:
    def __init__(self):
        self.thalamus = Thalamus()
        
        # Setup Window
        self.root = tk.Tk()
        self.root.title("Nexus AGI - Conscious Interface")
        self.root.geometry("800x600")
        self.root.configure(bg="#0d1117") # Hacker/Dark background
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, bg="#0d1117", fg="#c9d1d9", 
            font=("Consolas", 12), borderwidth=0, padx=15, pady=15
        )
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        self.chat_display.config(state=tk.DISABLED)
        
        # Start Redis listener in background thread
        threading.Thread(target=self.listen_to_brain, daemon=True).start()

    def append_text(self, sender, text, color_tag):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", ("sender",))
        self.chat_display.insert(tk.END, f"{text}\n\n", (color_tag,))
        
        # Colors configure karna
        self.chat_display.tag_config("sender", foreground="#58a6ff", font=("Consolas", 12, "bold"))
        self.chat_display.tag_config("user_color", foreground="#7ee787") # Green for User
        self.chat_display.tag_config("nexus_color", foreground="#d2a8ff") # Purple for AI
        
        self.chat_display.see(tk.END) # Auto-scroll to bottom
        self.chat_display.config(state=tk.DISABLED)

    def listen_to_brain(self):
        pubsub = self.thalamus.client.pubsub()
        # Hum user ki aawaz (audio_stream) aur AI ka text (ui_stream) sunenge
        pubsub.subscribe("audio_stream", "ui_stream")
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8') if isinstance(message['channel'], bytes) else message['channel']
                data = json.loads(message['data'])
                
                if channel == "audio_stream":
                    user_text = data.get("text", "")
                    if user_text:
                        self.root.after(0, self.append_text, "Vasu", user_text, "user_color")
                
                elif channel == "ui_stream":
                    nexus_text = data.get("text", "")
                    if nexus_text:
                        self.root.after(0, self.append_text, "Nexus", nexus_text, "nexus_color")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = NexusUI()
    ui.run()