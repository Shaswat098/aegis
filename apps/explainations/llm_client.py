import requests

OLLAMA_URL = "http://ollama:11434/api/generate"

def generate_llama_explaination(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",  
                "prompt": prompt,
                "stream": False
            },
            timeout=30   
        )

        if response.status_code == 200:
            try:
                result = response.json().get("response", "").strip()
                return result if result else None
            except Exception:
                return None

        print(f"[LLAMA ERROR] Status code: {response.status_code}")
        return None

    except requests.exceptions.Timeout:
        print("[LLAMA ERROR] Timeout")
        return None

    except Exception as e:
        print(f"[LLAMA ERROR] {str(e)}")
        return None