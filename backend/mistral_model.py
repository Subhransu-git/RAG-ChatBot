import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(context, question):
    prompt = f"""
Answer strictly using the context.
If the answer is not present, reply exactly:
"Information not found in the provided documents."

Context:
{context}

Question:
{question}

Answer (max 3 lines):
"""


    payload = {
        "model": "mistral:7b-instruct-q4_K_M",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 1024, #2048
            "num_predict": 100, #150
            "temperature": 0.0,
            "top_p":0.9,
            "repeat_penalty":1.1
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120   
    )
        response.raise_for_status()

        return response.json().get("response", "").strip()

    except requests.exceptions.Timeout:
        return "Model timeout. Please try again."

    except requests.exceptions.ConnectionError:
        return "Ollama server not running."

    except Exception as e:
        return f"Runtime Error: {str(e)}"

    return response.json()["response"].strip()