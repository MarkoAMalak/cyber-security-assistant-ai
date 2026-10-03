import os

os.environ.pop("GROQ_API_KEY", None)

import app  # noqa: E402


def test_build_messages_handles_both_history_formats():
    history = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
        ["legacy question", "legacy answer"],
    ]
    msgs = app.build_messages("what is phishing?", history)
    assert msgs[0]["role"] == "system"
    assert [m["role"] for m in msgs[1:]] == ["user", "assistant", "user", "assistant", "user"]
    assert msgs[-1]["content"] == "what is phishing?"


def test_respond_without_key_returns_clear_message():
    out = app.respond("hi", [], app.MODELS[0], 0.7, 256)
    assert "GROQ_API_KEY" in out
