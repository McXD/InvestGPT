import json
import re
import uuid
from functools import wraps
from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS
from flask_session import Session
import openai
import os
import traceback
from dotenv import load_dotenv
from api.map_risk_profile import map_risk_profile
from api.get_possible_reits import get_possible_reits
from api.get_portfolio import get_portfolio

load_dotenv()
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "supersecretkey"
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://127.0.0.1:3000"}})
Session(app)

SYSTEM_MESSAGE = open(os.path.join(os.path.dirname(__file__), 'system.txt'), "r").read()


def requires_session_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "session_token" not in session:
            session["session_token"] = str(uuid.uuid4())
        return f(*args, **kwargs)

    return decorated_function


def get_json(text):
    json_match = re.search(r"\{.*?\}", text, re.DOTALL)
    if json_match:
        json_string = json_match.group(0)
        data = json.loads(json_string)
        print("Got json:", text)
        return data
    return None


@app.route("/api/chat", methods=["POST"])
def chat_completion():
    data = request.json
    prompt = data.get("prompt")
    session_token = request.cookies.get("session_token", str(uuid.uuid4()))

    conversation_key = f"conversation_{session_token}"
    conversation = session.get(conversation_key, [{"role": "system", "content": SYSTEM_MESSAGE}])
    conversation.append({"role": "user", "content": prompt})

    chatgpt_payload = {
        "model": "gpt-3.5-turbo",
        "messages": conversation,
        "max_tokens": 300,
        "n": 1,
        "stop": None,
        "temperature": 0.8
    }

    try:
        chatgpt_response = openai.ChatCompletion.create(**chatgpt_payload)
        response_text = chatgpt_response.choices[0].message["content"].strip()
        data = get_json(response_text)
        admin_msg = "This is the site owner speaking."

        if data is not None:
            # interact with GPT for another round
            if 'age' in data:  # risk profile
                risk_value = map_risk_profile(data)
                reit_keys = get_possible_reits(risk_value)
                user_msg = f"Below are the REITs that match the user's risk profile: {', '.join(reit_keys)}. Please let the user select the REITs he wants to invest in. After you get the user's selection, respond with the json format, example: {{\"reit_keys\": [\"EQIX\", \"SBAC\"]}}."
            elif 'reit_keys' in data:  # reit selection
                reit_keys = data['reit_keys']
                weights = get_portfolio(reit_keys)
                user_msg = f"Below is the optimal portfolio: {', '.join([f'{reit_keys[i]}: {weights[i]}' for i in range(len(reit_keys))])}. Please let the user know the optimal portfolio."

            conversation.extend([
                {"role": "assistant", "content": response_text},
                {"role": "user", "content": f"{admin_msg} {user_msg}"}
            ])
            chatgpt_response = openai.ChatCompletion.create(**chatgpt_payload)
            response_text = chatgpt_response.choices[0].message["content"].strip()

        conversation.append({"role": "assistant", "content": response_text})
        session[conversation_key] = conversation

        response = make_response(jsonify({"text": response_text}))

        if not request.cookies.get("session_token"):
            response.set_cookie(
                "session_token",
                session_token,
                secure=False,  # Set to True when using HTTPS
                samesite="Lax",
                path="/",
            )

        print(response)
        return response

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Error communicating with ChatGPT API: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()
