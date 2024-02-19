import os

from fastapi import APIRouter, Depends
from openai import AsyncOpenAI

from ..dependencies import get_current_user
from ..schemas import OpenAIRequest, OpenAIResponse

router = APIRouter()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.post("/completion", response_model=OpenAIResponse)
async def openai_completion(request: OpenAIRequest, username: str = Depends(get_current_user)):
    print("username:", username)

    try:
        response = await client.chat.completions.create(model=request.engine,
                                                        messages=[
                                                            {"role": "system", "content": request.prompt}],
                                                        max_tokens=request.max_tokens,
                                                        temperature=request.temperature, top_p=request.top_p,
                                                        frequency_penalty=request.frequency_penalty,
                                                        presence_penalty=request.presence_penalty)
    except Exception as e:
        return {"error": str(e)}

    return {"completion": response.choices[0].message.content}
