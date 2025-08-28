
import json
import os
from fastapi import Request
from datetime import datetime, timezone
from openai import AsyncOpenAI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass
from openai import OpenAI
from pydantic_ai.agent import Agent
from openai import AsyncOpenAI
from prompt import prompt

load_dotenv()

app=FastAPI()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@dataclass
class Deps:
    openai: AsyncOpenAI

agent = Agent('openai:gpt-4o-mini',system_prompt=prompt, deps_type=Deps)

async def extract_info(url):
    print('mast')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup(['footer', 'header', 'nav', 'script', 'style']):
                element.decompose()
            text_content = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            cleaned_text = '\n'.join(lines)
            
            result = {
                "url": url,
                "content": cleaned_text,
                "title": soup.title.string if soup.title else "No title",
                "status": "success"
            }
            
            return json.dumps(result)
            
        except Exception as e:
            error_result = {
                "url": url,
                "error": str(e),
                "status": "error"
            }
            return json.dumps(error_result)

@app.post("/get-answer/")
async def get_answer(
    request: Request,
) -> StreamingResponse:
    print(request)
    body = await request.json()
    print(body)
    async def stream_response():
        now = datetime.now(timezone.utc)
        yield json.dumps({
            "role": "user",
            "timestamp": now.isoformat(),
        }).encode("utf-8") + b"\n"
        body = await request.json()
        user_prompt = body.get("url")
        info=await extract_info(user_prompt)
        print(user_prompt)
        print("-"*100)
        print(info)
        openai = AsyncOpenAI()
        deps = Deps(openai=openai)
        answer = await agent.run(info, deps=deps)
        print("answer:", answer.output)
        yield json.dumps({
        "role": "model",
        "timestamp": now.isoformat(),
        "content": answer.output,
        }).encode("utf-8") + b"\n"

    return StreamingResponse(stream_response(), media_type="text/plain")