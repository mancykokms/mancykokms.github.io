import json
import requests
import time
import os
import sys

API_KEY = "sk-459e319768154a98b65306dad2052efc"

API_URL = "https://api.deepseek.com/chat/completions"  # 请替换为正确 endpoint
MODEL_NAME = "deepseek-chat"  # 也可能是 deepseek-chat-v2 等
tick = "\u2705"
cross = "\u274C"

# Ensure stdout uses UTF-8 on Windows terminals to avoid UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def simplify_with_deepseek(word, definition):
    prompt = (
        f"从以下释义中提取最简洁、常见的中文关键词（2到4个），可并列，适合词典展示。\n\n"
        f"词语：{word}\n"
        f"释义：{definition}\n"
        f"简化关键词："
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        # print debug if needed
        # Uncomment the next line to see the full API response for debugging
        # print(f"DEBUG: API response for '{word}':\n{json.dumps(result, ensure_ascii=False, indent=2)}\n")
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"{cross} {word} failed: {e}")
        return ""

def process_vocab_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        vocab_list = json.load(f)

    new_data = []
    for idx, entry in enumerate(vocab_list):
        if not isinstance(entry, list) or len(entry) != 2:
            continue
        word, definition = entry
        simplified = simplify_with_deepseek(word, definition)
        new_data.append([word, definition, simplified])
        print(f"[{idx+1}] {word} {tick} {simplified}")
        time.sleep(1.2)  # Rate limit buffer

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

# Run script
if __name__ == "__main__":
    input_path = "a.json"
    output_path = "simplified_vocab.json"
    process_vocab_file(input_path, output_path)

    print(f"{tick} 完成！简化词汇已保存到 {output_path}")
    