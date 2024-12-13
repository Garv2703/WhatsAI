from flask import Flask, request, jsonify
import google.generativeai as genai, os, requests
from google.generativeai.types import HarmBlockThreshold, HarmCategory

app = Flask(__name__)
# app.secret_key = 'flask-insecure-ot%!h9epy)g9scdb^$)ymmt&#@ca=pyjg+7-p_yh89di6g0^c5'

# WhatsApp API credentials (use environment variables in production)
API_URL = "https://api.whatsapp.com/send_message"
ACCESS_TOKEN = "your_access_token"
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
)

history=[
    {'role': 'user', 'parts': 'Hello!'},
    {'role': 'model', 'parts': "Hi babe! Anything hot and spicy for tonight?"},
]
chat = model.start_chat(history=history)
    

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message', {}).get('text')
    sender_id = data.get('sender', {}).get('id')
    
    if message and sender_id:
        reply = generate_reply(message)
        send_message(sender_id, reply)
    return jsonify({"status": "success"}), 200

def generate_reply(message):
    global chat
    response = chat.send_message(
        message,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    resp = response.text
    return resp

def send_message(to, message):
    # Function to send a message via WhatsApp API
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "to": to,
        "message": {"text": message}
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.status_code

if __name__ == '__main__':
    app.run(port=5000, debug=True)
