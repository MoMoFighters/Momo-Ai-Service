from fastapi import APIRouter

"""
텍스트를 벡터로 바꿔주는 /embed 엔드포인트 골격
나중에 Gemini 임베딩 API 가 여기서 호출되게 된다.
"""

from app.schema.embed_schema import EmbedRequest, EmbedResponse
from app.service.embedding_service import embed_document

router = APIRouter(prefix="/embed", tags=["embed"])


@router.post("", response_model=EmbedResponse)
def create_embedding(request: EmbedRequest):
    embedding = embed_document(request.text)
    return EmbedResponse(embedding=embedding)