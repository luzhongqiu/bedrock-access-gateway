from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request, HTTPException, status
from fastapi.responses import StreamingResponse

from api.models.bedrock import BedrockModel, get_bedrock_clients
from api.schema import ChatRequest, ChatResponse, ChatStreamResponse
from api.setting import DEFAULT_MODEL

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/completions", response_model=ChatResponse | ChatStreamResponse, response_model_exclude_unset=True)
async def chat_completions(
    request: Request,
    chat_request: Annotated[
        ChatRequest,
        Body(
            examples=[
                {
                    "model": "anthropic.claude-3-sonnet-20240229-v1:0",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello!"},
                    ],
                }
            ],
        ),
    ],
):
    if chat_request.model.lower().startswith("gpt-"):
        chat_request.model = DEFAULT_MODEL

    # 获取动态生成的bedrock客户端
    bedrock_runtime, bedrock_client = get_bedrock_clients(request)

    # Exception will be raised if model not supported.
    model = BedrockModel(bedrock_runtime, bedrock_client)
    model.validate(chat_request)
    if chat_request.stream:
        return StreamingResponse(content=model.chat_stream(chat_request), media_type="text/event-stream")
    return await model.chat(chat_request)
