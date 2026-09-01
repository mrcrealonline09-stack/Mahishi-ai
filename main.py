from flask import Flask, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return "Mahishi AI LIVE hai! /chat/hello kholo"

@app.route('/chat/<path:sawal>')
def chat(sawal):
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Tum Mahishi Bihar ka AI ho"},
                {"role": "user", "content": sawal}
            ],
            model="llama-3.1-8b-instant",
        )
        return jsonify({"jawab": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
