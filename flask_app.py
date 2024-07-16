from flask import Flask, request, jsonify
from transformers import pipeline
from anthropic import Anthropic
import os

app = Flask(__name__)

# 여러 언어 모델 초기화
models = {
    "model": pipeline("text-generation", model="gpt2"),
}

CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not CLAUDE_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.")

anthropic_client = Anthropic(api_key=CLAUDE_API_KEY)


@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "")
    max_length = data.get("max_length", 50)
    model_name = data.get("model", "model")
    messages = data.get("messages", [])

    if model_name == "api":
        return generate_claude_response(prompt, messages)
    elif model_name in models:
        model = models[model_name]
        generated_text = model(prompt, max_length=max_length, num_return_sequences=1)[
            0
        ]["generated_text"]
        return jsonify({"generated_text": generated_text})
    else:
        return jsonify({"error": "Invalid model name"}), 400


def generate_claude_response(prompt, messages):
    claude_messages = [
        {"role": msg["role"], "content": msg["content"]} for msg in messages
    ]

    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620", max_tokens=1000, messages=claude_messages
    )
    generated_text = message.content[0].text
    return jsonify({"generated_text": generated_text})


def run_flask():
    app.run(port=5000)


if __name__ == "__main__":
    run_flask()
