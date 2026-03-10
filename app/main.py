from fastapi import FastAPI, Request, Response
from app.proxy import forward_request, process_response
from app.store import SessionStore
import asyncio

app = FastAPI(
    title="IronLayer API",
    description="The Security Layer for AI. Sanitizes PII and Secrets before reaching external models.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    async def cleanup_task():
        while True:
            SessionStore.cleanup()
            await asyncio.sleep(60)
    asyncio.create_task(cleanup_task())

# Add operation_id to suppress the warning
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], operation_id="catch_all")
async def catch_all(request: Request, path: str):
    # 1. Read Request
    body = await request.body()
    headers = dict(request.headers)
    
    # 2. Forward & Sanitize
    upstream_response = await forward_request(
        method=request.method,
        path=path,
        headers=headers,
        body=body
    )
    
    # 3. Process & Desanitize
    final_body = await process_response(upstream_response, path)
    
    # 4. Filter Headers
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
    response_headers = {
        k: v for k, v in upstream_response.headers.items() 
        if k.lower() not in excluded_headers
    }
    
    # 5. Return
    return Response(
        content=final_body,
        status_code=upstream_response.status_code,
        headers=response_headers
    )