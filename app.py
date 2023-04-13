from flask import Flask, request
import openai
import json
import requests
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{incoming_msg}"},
        ],
        "max_tokens": 100,
        "n": 1,
        "stop": None,
        "temperature": 0.5,
    }

    chat_gpt_response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data),
    )
    print(chat_gpt_response.text)  # Add this line to print the API response

    chat_gpt_response_json = chat_gpt_response.json()

    if "choices" in chat_gpt_response_json:
        reply = chat_gpt_response_json["choices"][0]["message"]["content"].strip()
    else:
        reply = "Sorry, there was an issue processing your request. Please try again later."

    response.message(reply)

    return str(response)

@app.route("/", methods=["GET"])
def index():
    return "Hello Folks, Welcome to Priyank's WhatsApp bot ! If you see this it is a proof that bot is ready to serve you."

if __name__ == "__main__":
    app.run(debug=True)