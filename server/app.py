from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import datetime
from prompts import *
from chatbot import *
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from openai import OpenAI
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=openai_api_key)
account_sid = twilio_account_sid
auth_token = twilio_auth_token
client_twilio = TwilioClient(account_sid, auth_token)


def create_new_assistant(bot_name):
    new_assistant = client.beta.assistants.create(
        name=bot_name,
        instructions="You are a personal chat assistant.",
        model="gpt-3.5-turbo-1106"
    )
    return new_assistant



bots_data = {
    "math": {
        "assistant": create_new_assistant("Math Tutor"),
        "conversation": [],
    },
    "science": {
        "assistant": create_new_assistant("Science Assistant"),
        "conversation": [],
    },
    "music": {
        "assistant": create_new_assistant("Music Bot"),
        "conversation": [],
    },
}


def get_assistant():
    bot_id = "asst_ebPdWTSkDezIDh61de0wbyWC"
    return global_assistant 

def get_conversation():
    return conversation 

# @app.route("/api/user_input/<bot_id>", methods=['POST', 'GET'])
# def get_user_input(bot_id):
#     user_input = request.get_json()

#     if 'message' not in user_input:
#         return jsonify({"error": "Missing 'message' field"}), 400
    
#     if not user_input['message'].strip():
#         return jsonify({"error": "'message' should not be an empty string"}), 400
    
#     message = user_input['message']

#     bot_data = bots_data.get(bot_id)
#     if not bot_data:
#         return jsonify({"error": "Bot not found"}), 404
    
#     assistant = bot_data["assistant"]
#     conversation = bot_data["conversation"]
#     result = start_assistant(message, assistant, conversation)

#     conversation.append({"role": "user", "content": message})
#     conversation.append({"role": "assistant", "content": result})

#     return jsonify({"message": result, "user_input": message})

@app.route("/api/user_input", methods=['POST', 'GET'])
def get_user_input():
  user_input = request.get_json()

  if 'message' not in user_input:
    return jsonify({"error": "Missing 'message' field"}), 400
  
  if not user_input['message'].strip():
    return jsonify({"error": "'message' should not be an empty string"}), 400
  
  message = user_input['message']

  # Use the single bot instance
  assistant = get_assistant()  # Assuming a function to retrieve single assistant
  conversation = get_conversation()  # Assuming a function to retrieve single conversation history

  result = start_assistant(message, assistant, conversation)

  conversation.append({"role": "user", "content": message})
  conversation.append({"role": "assistant", "content": result})

  return jsonify({"message": result, "user_input": message})



@app.route('/api/conversation_history', methods=['GET'])
def get_conversation_history():
  conversation = get_conversation()  # Assuming a function to retrieve single conversation history

  start = int(request.args.get('start', 0))
  end = int(request.args.get('end', len(conversation)))

  if start < 0:
    start = 0
  if end > len(conversation):
    end = len(conversation)

  history_part = conversation[start:end]

  return jsonify(history_part)



@app.route('/api/add_message/<bot_id>', methods=['POST'])
def add_message(bot_id):
    data = request.get_json()
    message = data.get('message')
    
    if message:
        conversation.append(message)
        return jsonify({"message": "Message ajouté avec succès."})
    else:
        return jsonify({"error": "Message vide ou manquant."}), 400


twilio_numbers = {
    "+14155238886": {
        "assistant": create_new_assistant("Math Tutor"),
        "conversation": [],
    },
    "+14155238887": {
        "assistant": create_new_assistant("Science Assistant"),
        "conversation": [],
    },
    "+14155238888": {
        "assistant": create_new_assistant("Music Bot"),
        "conversation": [],
    },
}

@app.route('/api/whatsapp_twilio', methods=['POST'])
def whatsapp_reply():
    query = request.form['Body'].lower()
    twilio_number = request.form['To'].replace('whatsapp:', '').strip().lower()
    if twilio_number not in twilio_numbers:
        return jsonify({"error": "Bot not found"}), 404
    assistant_info = twilio_numbers.get(twilio_number)
    assistant = assistant_info["assistant"]
    conversation = assistant_info["conversation"]
    result = start_assistant(query, assistant, conversation)
    twilio_response = MessagingResponse()
    twilio_response.message(result, From=f"whatsapp:{twilio_number}")
    response_xml = str(twilio_response)
    return response_xml


if __name__ == '__main__':
    app.run()