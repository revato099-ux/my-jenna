from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

@app.route('/api/chat', methods=['POST'])
def chat():
    if not REPLICATE_TOKEN:
        return jsonify({"response": "Token topilmadi! Renderda Environment Variables qo'shing."}), 400

    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"response": "Xabar bo'sh!"}), 400

    try:
        resp = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {REPLICATE_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "version": "e5582ad7aaa86a2b000a90d6c7c59c51d7a9fcab33529f2477a292c73fae0551",
                "input": {
                    "prompt": f"""Siz JENNA - o'zbek tilidagi do'stona va aqlli AI yordamchisiz. 
Javoblaringiz qisqa, tabiiy va foydali bo'lsin.

Foydalanuvchi: {user_message}
JENNA:""",
                    "max_tokens": 200,
                    "temperature": 0.7
                }
            },
            timeout=40
        )
        data = resp.json()
        output = data.get("output", "")
        if isinstance(output, list):
            output = "".join(output)
        return jsonify({"response": output.strip() or "Tushundim!"})
    except Exception as e:
        return jsonify({"response": "Tarmoq xatosi yuz berdi. Keyinroq urinib ko'ring."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
