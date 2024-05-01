from openai import OpenAI
import time
from prompts import *
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client =  OpenAI(api_key=openai_api_key)
account_sid = twilio_account_sid
auth_token = twilio_auth_token
client_twilio = Client(account_sid, auth_token)

conversation = []  # Maintain conversation history for the single bot

thread_id = None  # Store the single thread ID for the conversation

def add_user_message_to_conversation(user_input):
  conversation.append({
      "role": "user",
      "content": user_input
  })

def add_assistant_message_to_conversation(bot_message):
  conversation.append({
      "role": "assistant",
      "content": bot_message
  })

def get_last_assistant_response():
  for message in reversed(conversation):
    if message["role"] == "assistant":
      return message["content"]
  return None  # If no assistant response found

def get_thread_id():
  global thread_id
  if not thread_id:
    thread = client.beta.threads.create()
    thread_id = thread.id
  return thread_id

def wait_for_assistant_completion(run_id):
  assistant_complete = False
  while not assistant_complete:
    time.sleep(1)
    run_status = client.beta.threads.runs.retrieve(
        run_id=run_id
    )
    if run_status.status == 'completed':
      assistant_complete = True

def start_assistant(user_input):
  message = client.beta.threads.messages.create(
      thread_id=get_thread_id(),
      role="user",
      content=user_input,
  )

  user_message = message.content[0].text.value
  add_user_message_to_conversation(user_message)

  run = client.beta.threads.runs.create(
      thread_id=get_thread_id(),
      assistant_id=asst_ebPdWTSkDezIDh61de0wbyWC,  # Replace with your single assistant ID
      instructions=chatbot_instructions,
  )

  wait_for_assistant_completion(run.id)

  messages = client.beta.threads.messages.list(
      thread_id=get_thread_id()
  )

  for msg in reversed(messages.data):
    if msg.role == 'assistant':
      bot_message = msg.content[0].text.value
      add_assistant_message_to_conversation(bot_message)
      return bot_message


# def get_or_create_thread_id(conversation):
#     for item in reversed(conversation):
#         if "thread_id" in item:
#             return item["thread_id"]
        
#     thread = client.beta.threads.create()
#     thread_id = thread.id
#     conversation.append({"thread_id": thread_id})
#     return thread.id


def send_message(recipient, user_message):
    message = client_twilio.messages.create(
        from_='whatsapp:+14155238886',
        body=user_message,
        to=recipient
    )

    print("Message sent to recipient:", recipient)
    print("Message content:", user_message)
    print("Message SID:", message.sid)
