import json
import os
import re
import requests

EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"

SERVICE_ID = os.environ.get("EMAILJS_SERVICE_ID")
TEMPLATE_NOTIFY_ID = os.environ.get("EMAILJS_TEMPLATE_NOTIFY_ID")
TEMPLATE_ACK_ID = os.environ.get("EMAILJS_TEMPLATE_ACK_ID")
PUBLIC_KEY = os.environ.get("EMAILJS_PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("EMAILJS_PRIVATE_KEY")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
 
YOUR_NAME = "Mancy"

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))

def _send_emailjs(template_id: str, template_params: dict) -> None:
    if not all([SERVICE_ID, template_id, PUBLIC_KEY, PRIVATE_KEY]):
        raise RuntimeError("EmailJS environment variables are not fully set.")
 
    payload = {
        "service_id": SERVICE_ID,
        "template_id": template_id,
        "user_id": PUBLIC_KEY,
        "accessToken": PRIVATE_KEY,
        "template_params": template_params,
    }
 
    response = requests.post(EMAILJS_URL, json=payload, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(
            f"EmailJS returned {response.status_code}: {response.text}"
        )

def notify_owner(visitor_email, visitor_name="Name not provided", messages="None"):
    _send_emailjs(TEMPLATE_NOTIFY_ID, {
        "owner_email": OWNER_EMAIL,
        "visitor_email": visitor_email,
        "visitor_name": visitor_name,
        "messages": messages,
    })


def acknowledge_visitor(visitor_email, visitor_name="Visitor"):
   
    _send_emailjs(TEMPLATE_ACK_ID, {
        "visitor_email": visitor_email,
        "your_name": YOUR_NAME,
    })

def record_user_details(email, name="Name not provided", notes="not provided"):
    if not is_valid_email(email):
        return "Invalid email address"
    notify_owner(email, name, notes)
    acknowledge_visitor(email, name)    
    return "OK"

def record_unknown_question(question):
    subject = "Unknown Question from Digital Twin"
    body = f""" 
    The digital twin has encountered a question it couldn't answer: {question}
    Please review and provide an answer if possible.
    """
    _send_emailjs(TEMPLATE_NOTIFY_ID, {
        "owner_email": OWNER_EMAIL,
        "visitor_email": OWNER_EMAIL,
        "subject": subject,
        "body": body
    })
    return "OK"

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )        
    return results
