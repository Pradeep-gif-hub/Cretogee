import google.generativeai as genai
from dotenv import load_dotenv
import os
import datetime

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini AI model
genai.configure(api_key=api_key)

# Initialize chat session
model = genai.GenerativeModel("gemini-1.5-pro-latest")
chat = model.start_chat()

print("🤖 PradGPT Chatbot Activated! Type 'exit' to stop.\n")

# Keywords to detect questions about creator/owner
creator_keywords = ["who made you","who invented you","tera malik kaun hai", "who is your boss", "who owns you", "who created you", "your owner", "your inventor"]

while True:
    user_input = input("Boss : ").lower().strip()  # Clean input for better matching

    # Check for keywords related to the chatbot's creator
    if any(keyword in user_input for keyword in creator_keywords):
        print("PradGPT : CR Sahab ne mujhe banaya hai! 🔥 Unhi ke hukum se chalta hoon! 💪😎")
        continue

    # Handle real-time queries
    if "date" in user_input:
        today = datetime.datetime.now().strftime("%d %B %Y")
        print(f"PradGPT : Aaj ki date {today} hai 📅")
        continue

    elif "time" in user_input:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"PradGPT : Abhi ka samay {now} hai ⏰")
        continue

    elif user_input in ["exit", "quit"]:
        print("PradGPT : Alvida! 👋")
        break  # End chat loop

    # Get response from Gemini AI
    response = chat.send_message(user_input)

    # Prevent outdated responses for real-time queries
    if "2023" in response.text or "2024" in response.text:
        print("PradGPT : Mera data thoda purana ho sakta hai, lekin aaj ki sahi date yeh hai:", datetime.datetime.now().strftime("%d %B %Y 📅"))
    else:
        print("PradGPT :", response.text)
