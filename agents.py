import openai
import base64
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_id_document_with_llm(file_path: str) -> dict:
    with open(file_path, "rb") as f:
        image_bytes = f.read()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a document parsing assistant. Extract guest information from an image of an ID as a JSON."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the following fields as a JSON object with keys: first_name, last_name, dob (YYYY-MM-DD), pob (place of birth)."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
                ]
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()
    json_match = re.search(r'\{[\s\S]*?\}', content)
    cleaned = json_match.group(0).strip() if json_match else content

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse LLM response as JSON:", repr(content))
        return {
            "first_name": "",
            "last_name": "",
            "dob": "",
            "pob": ""
        }

def is_document_submission(message: str) -> bool:
    return message.strip().endswith(".png") or message.strip().endswith(".jpg")
