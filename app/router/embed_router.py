from fastapi import APIRouter

"""
텍스트를 벡터로 바꿔주는 /embed 엔드포인트 골격
나중에 Gemini 임베딩 API 가 여기서 호출되게 된다.
"""

from app.schema.embed_schema import EmbedRequest, EmbedResponse

router = APIRouter(prefix="/embed", tags=["embed"])


@router.post("", response_model=EmbedResponse)
def create_embedding(request: EmbedRequest):
    # TODO: Gemini 임베딩 API 연동 (다음 작업)
    return EmbedResponse(embedding=[])