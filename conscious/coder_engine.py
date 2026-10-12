import os
import re
import subprocess
from groq import Groq
from dotenv import load_dotenv

class AutoCoder:
    def __init__(self):
        print("💻 [CODER ENGINE] AI Software Engineer is Online (Powered by GROQ SDK).")
        
        # 🔑 APIS - Yahan apni Groq API key daalo
        self.GROQ_API_KEY = os.getenv("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")
        
        # Initialize the official Groq client
        self.client = Groq(api_key=self.GROQ_API_KEY)

    def call_smart_llm(self, prompt):
        """Official Groq SDK ka use karke LLM ko call karna"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an elite Python developer. Output ONLY valid python code inside ```python blocks. Do NOT write any explanations, greetings, or text outside the code block."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                # 🚀 UPDATE: Screenshot wale Playground se exact working model name
                model="openai/gpt-oss-120b", 
                temperature=0.2,
            )
            
            print("⚡ [API] Code generated successfully using Groq.")
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            print(f"❌ [GROQ CRITICAL FAIL] Error: {e}")
            return None

    def write_and_heal_code(self, feature_name, user_request):
        """The Auto-Healer Loop: Write -> Test -> Fix Error"""
        # Ensure skills folder exists
        os.makedirs("skills", exist_ok=True)
        file_path = f"skills/{feature_name}.py"
        
        prompt = f"""
        Create a standalone Python script for the following task: '{user_request}'.
        - It must contain a function called 'run()' that executes the main logic.
        - Print the output to the console.
        - Do NOT use input() prompts, hardcode any required test values.
        """
        
        max_tries = 3
        for attempt in range(max_tries):
            print(f"🛠️ [CODER] Attempt {attempt + 1}/{max_tries}: Writing code for '{feature_name}'...")
            llm_response = self.call_smart_llm(prompt)
            
            if not llm_response:
                return "Bhai, API ne respond nahi kiya."

            # Code ko Markdown blocks se nikalna
            code_match = re.search(r'```(?:python)?\n(.*?)```', llm_response, re.DOTALL | re.IGNORECASE)
            code = code_match.group(1).strip() if code_match else llm_response.replace('```', '').strip()

            # Code save karna
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # --- 🛡️ THE SANDBOX TEST (Self-Healing) ---
            print(f"🧪 [CODER] Testing '{feature_name}.py' for Syntax/Runtime errors...")
            try:
                result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("✅ [CODER] Success! Code is bug-free and ready to use.")
                    return f"Feature '{feature_name}' successfully added and tested!\nOutput:\n{result.stdout.strip()}"
                else:
                    error_msg = result.stderr.strip()
                    print(f"🐛 [CODER BUG DETECTED]: {error_msg.split()[-1][:100]}... Healing now.")
                    
                    # Error LLM ko wapas bhejna taaki wo khud fix kare
                    prompt += f"\n\nWait, your previous code threw this ERROR when executed:\n{error_msg}\n\nAnalyze the error, fix the bug, and rewrite the FULL correct code inside ```python blocks."
                    
            except subprocess.TimeoutExpired:
                print("⏳ [CODER BUG] Infinite loop or stuck execution detected. Healing...")
                prompt += "\n\nError: Your code took too long to execute (Timeout). Remove any input() calls, infinite while loops, or slow network calls. Rewrite the code."

        # Agar 3 attempt ke baad bhi fix nahi hua, toh kachra code hata do
        if os.path.exists(file_path):
            os.remove(file_path)
        return "Bhai, mene 3 baar try kiya par code me bugs the. System safety ke liye file delete kar di hai."

if __name__ == "__main__":
    # Test karne ke liye
    coder = AutoCoder()
    print(coder.write_and_heal_code("test_math", "Write a python script to calculate the factorial of 5 and print it."))