"""
Test ChatAnywhere supported models
测试 ChatAnywhere 支持的模型
"""

from openai import OpenAI
import json

# Load config
with open("api_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

api_key = config["claude"]["api_key"]
base_url = config["claude"]["base_url"]

client = OpenAI(base_url=base_url, api_key=api_key)

# Test different model names
test_models = [
    "gpt-3.5-turbo",  # Most common, should work
    "gpt-4",
    "gpt-4-turbo",
    "claude",
    "claude-3-opus",
    "claude-3-5-sonnet",
    "claude-3-sonnet",
]

print("Testing ChatAnywhere models...")
print("=" * 60)

for model in test_models:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5
        )
        print(f"[OK] {model}: {response.choices[0].message.content}")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not supported" in error_msg.lower():
            print(f"[FAIL] {model}: Not supported")
        else:
            print(f"[ERROR] {model}: {error_msg[:100]}")

print("=" * 60)
print("\nUse the models that show [OK] in your api_config.json")
