import json
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def print_json(obj):
    json_str = obj.model_dump_json()
    parsed_json = json.loads(json_str)
    return parsed_json

api_key = os.environ.get('OPENAI_API_KEY')
print(api_key)
client = OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
    name="Exercise Bot",
    instructions="you are smart assistant who can create different exercise schedules",
    model="gpt-4-1106-preview",
)
print_json(assistant)

thread = client.beta.threads.create()
print(print_json(thread))