import os

folders = [
    "memory",        # Database & State (Thalamus, VectorDB, Graph)
    "sensors",       # Inputs (Vision, Audio)
    "actors",        # Outputs (Speech, Actions)
    "subconscious",  # System 1 (Fast Vector Reflexes)
    "conscious",     # System 2 (Slow LLM & Math Engine)
    "utils"          # Helper functions
]

files = {
    "": ["main.py", "requirements.txt", ".env"],
    "memory": ["__init__.py", "redis_broker.py", "vector_db.py", "graph_db.py"],
    "sensors": ["__init__.py", "vision_node.py", "audio_in.py"],
    "actors": ["__init__.py", "audio_out.py"],
    "subconscious": ["__init__.py", "reflex_engine.py"],
    "conscious": ["__init__.py", "logic_engine.py", "math_engine.py"]
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for folder, file_list in files.items():
    for file in file_list:
        path = os.path.join(folder, file) if folder else file
        with open(path, "w") as f:
            pass

print("Nexus Brain Structure Created Successfully!")