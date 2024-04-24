import anthropic
import time
from prompts import *
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

# openai_api_key = os.getenv('OPENAI_API_KEY')
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = anthropic.Client(anthropic.CONST)
account_sid = twilio_account_sid
auth_token = twilio_auth_token
client_twilio = Client(account_sid, auth_token)

conversation = []

def add_user_message_to_conversation(user_input, conversation):
    conversation.append({
        "role": "user",
        "content": user_input
    })

def add_assistant_messages_to_conversation(result, conversation):
    for msg in result.output:
        conversation.append({"role": "assistant", "content": msg})

def get_last_assistant_response(result):
    return result.output[-1]
        
def get_thread_messages(thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    return messages

def wait_for_assistant_completion(thread_id, run_id):
    assistant_complete = False
    while not assistant_complete:
        time.sleep(1)
        run_status = client.get_instruction_following_run(run_id)
        if run_status.status == 'completed':
            assistant_complete = True
    return run_status.result

def start_assistant(user_input, assistant, conversation):
    thread_id = get_or_create_thread_id(conversation)
    run_id = client.start_instruction_following(
        assistant=assistant, 
        threads=[anthropic.InstructionFollowingThread(
            instruction_string=user_input, 
            thread_id=thread_id
        )]
    )
    result = wait_for_assistant_completion(thread_id, run_id)
    add_user_message_to_conversation(user_input, conversation)
    add_assistant_messages_to_conversation(result, conversation)
    return get_last_assistant_response(result)


def get_or_create_thread_id(conversation):
    for item in reversed(conversation):
        if "thread_id" in item:
            return item["thread_id"]
        
    thread = client.beta.threads.create()
    thread_id = thread.id
    conversation.append({"thread_id": thread_id})
    return thread.id


def send_message(recipient, user_message):
    message = client_twilio.messages.create(
        from_='whatsapp:+14155238886',
        body=user_message,
        to=recipient
    )

    print("Message sent to recipient:", recipient)
    print("Message content:", user_message)
    print("Message SID:", message.sid)
