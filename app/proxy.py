import httpx
import json
from app.config import settings
from app.sanitizer import sanitize_text, desanitize_text

client = httpx.AsyncClient(timeout=60.0)

async def forward_request(method: str, path: str, headers: dict, body: bytes):
    url = f"{settings.base_url}/{path}"
    
    headers.pop('host', None)
    headers.pop('content-length', None)
    headers.pop('authorization', None) 

    final_headers = {
        "Authorization": f"Bearer {settings.API_KEY}",
        "Content-Type": "application/json",
        **settings.headers
    }
    
    final_headers.update(headers)

    if "chat/completions" in path and body:
        try:
            data = json.loads(body)
            
            # Force free model if needed
            if "model" in data:
                if data["model"].startswith("gpt"):
                    print(f"[IronLayer] Swapping model {data['model']} to free model...")
                    data["model"] = "arcee-ai/trinity-large-preview:free"
            
            if "messages" in data:
                # --- THE LOGIC FIX ---
                # Inject a system instruction to force placeholder preservation
                system_instruction = {
                    "role": "system",
                    "content": "CRITICAL SECURITY INSTRUCTION: You must preserve all placeholders (e.g., <SECRET_123>, <EMAIL_ADDRESS_abc>) exactly as written in your response. Do not rephrase or remove them."
                }
                # Insert at the beginning of the conversation
                data["messages"].insert(0, system_instruction)
                # ---------------------

                for message in data["messages"]:
                    if isinstance(message.get("content"), str):
                        # Skip the system instruction we just added
                        if "CRITICAL SECURITY INSTRUCTION" in message["content"]:
                            continue
                        message["content"] = sanitize_text(message["content"])
                
                print(f"[IronLayer] Secure payload sent to provider.")
                
                body = json.dumps(data).encode('utf-8')
        except Exception as e:
            print(f"!!! [IronLayer] CRITICAL ERROR: Sanitization Failed. Reason: {e}")
            raise e 

    response = await client.request(
        method=method,
        url=url,
        headers=final_headers,
        content=body
    )
    
    if response.status_code >= 400:
        print(f"\n!!! UPSTREAM ERROR ({response.status_code}) !!!")
        print(response.text)
        print("!!! END ERROR !!!\n")

    return response

async def process_response(response: httpx.Response, path: str):
    if response.status_code == 200 and "chat/completions" in path:
        try:
            data = response.json()
            
            if "choices" in data:
                for choice in data["choices"]:
                    if "message" in choice and "content" in choice["message"]:
                        choice["message"]["content"] = desanitize_text(choice["message"]["content"])
            
            return json.dumps(data).encode('utf-8')
        except Exception as e:
            print(f"Error desanitizing: {e}")
            return response.content
    
    return response.content