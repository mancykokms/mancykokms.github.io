from dotenv import load_dotenv
import os

load_dotenv(override=True)

from openai import OpenAI
from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES
import gradio as gr

MODEL_NAME = "deepseek-chat"

openai = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(response.choices[0].message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    content = response.choices[0].message.content.strip()
    import json, re
    # Strip markdown code fences
    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", content)
    cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    # Try direct parse
    try:
        return json.loads(cleaned)["reply"]
    except Exception:
        pass
    # Fall back: extract first {...} block from the string
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())["reply"]
        except Exception:
            pass
    return content

demo = gr.ChatInterface(
    chat,
    examples=EXAMPLES,
    title="Mancy's Digital Twin",
    description="Talk to my AI about my career",
    chatbot=gr.Chatbot(show_label=False),
)

demo.launch(
    css=CSS,
    js=JS,
    theme=gr.themes.Soft(primary_hue="violet", neutral_hue="slate"),
)