import os

import gradio as gr
from groq import Groq

SYSTEM_PROMPT = """You are a cybersecurity expert chatbot.
Provide accurate, structured, and practical responses to questions related to
cyber security, including threats, vulnerabilities, best practices, and prevention techniques.
Maintain a professional and educational tone.
"""

MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

_client = None


def get_client():
    """Create the Groq client lazily so the app starts even without a key."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return None
        _client = Groq(api_key=api_key)
    return _client


def build_messages(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history or []:
        if isinstance(turn, dict):  # "messages" format
            if turn.get("role") in ("user", "assistant") and turn.get("content"):
                messages.append({"role": turn["role"], "content": str(turn["content"])})
        else:  # legacy [user, assistant] pairs
            user_msg, bot_msg = turn[0], turn[1] if len(turn) > 1 else None
            if user_msg:
                messages.append({"role": "user", "content": str(user_msg)})
            if bot_msg:
                messages.append({"role": "assistant", "content": str(bot_msg)})
    messages.append({"role": "user", "content": message})
    return messages


def respond(message, history, model, temperature, max_tokens):
    client = get_client()
    if client is None:
        return ("⚠️ GROQ_API_KEY is not set. Add it as an environment variable "
                "(or a Space secret) and restart the app.")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=build_messages(message, history),
            temperature=temperature,
            max_completion_tokens=int(max_tokens),
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    title="🔐 Cyber Security Assistant AI",
    description="Ask questions about cyber threats, security best practices, and protection strategies.",
    additional_inputs=[
        gr.Dropdown(choices=MODELS, value=MODELS[0], label="Model",
                    info="Select the AI model to use"),
        gr.Slider(minimum=0, maximum=2, value=0.7, step=0.1, label="Temperature",
                  info="Lower = more focused, higher = more creative"),
        gr.Slider(minimum=256, maximum=8192, value=2048, step=256, label="Max Tokens",
                  info="Maximum length of the response"),
    ],
    examples=[
        ["What is phishing and how can organizations prevent it?"],
        ["Explain ransomware attacks and mitigation strategies"],
        ["What are best practices for securing a corporate network?"],
    ],
    theme="soft",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
