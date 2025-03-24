from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request, HTTPException, status

from api.models.bedrock import get_embeddings_model, get_bedrock_clients
from api.schema import EmbeddingsRequest, EmbeddingsResponse
from api.setting import DEFAULT_EMBEDDING_MODEL

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
)


@router.post("", response_model=EmbeddingsResponse)
async def embeddings(
    request: Request,
    embeddings_request: Annotated[
        EmbeddingsRequest,
        Body(
            examples=[
                {
                    "model": "cohere.embed-multilingual-v3",
                    "input": ["Your text string goes here"],
                }
            ],
        ),
    ],
):
    if embeddings_request.model.lower().startswith("text-embedding-"):
        embeddings_request.model = DEFAULT_EMBEDDING_MODEL
    
    # 获取动态生成的bedrock客户端
    bedrock_runtime, _ = get_bedrock_clients(request)
    
    # Exception will be raised if model not supported.
    model = get_embeddings_model(embeddings_request.model, bedrock_runtime)
    return model.embed(embeddings_request)
