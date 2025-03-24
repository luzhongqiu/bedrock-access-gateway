from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from api.models.bedrock import BedrockModel, get_bedrock_clients
from api.schema import Model, Models

router = APIRouter(
    prefix="/model",
    tags=["model"],
)


async def validate_model_id(model_id: str, bedrock_runtime, bedrock_client):
    model = BedrockModel(bedrock_runtime, bedrock_client)
    if model_id not in model.list_models():
        raise HTTPException(status_code=500, detail="Unsupported Model Id")


@router.get("", response_model=Models)
async def list_models(request: Request):
    # 获取动态生成的bedrock客户端
    bedrock_runtime, bedrock_client = get_bedrock_clients(request)
    model = BedrockModel(bedrock_runtime, bedrock_client)
    model_list = [Model(id=model_id) for model_id in model.list_models()]
    return Models(data=model_list)


@router.get(
    "/{model_id}",
    response_model=Model,
)
async def get_model(
    request: Request,
    model_id: Annotated[
        str,
        Path(description="Model ID", example="anthropic.claude-3-sonnet-20240229-v1:0"),
    ],
):
    # 获取动态生成的bedrock客户端
    bedrock_runtime, bedrock_client = get_bedrock_clients(request)
    await validate_model_id(model_id, bedrock_runtime, bedrock_client)
    return Model(id=model_id)
