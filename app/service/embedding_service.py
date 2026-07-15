from google import genai
from google.genai import types

from app.config.settings import settings

"""
텍스트 -> Gemini 임베딩 벡터 변환.
자바로 치면 외부 API(OAuth 서버 등)를 호출하는 Adapter와 같은 위치.
"""

EMBEDDING_MODEL = "gemini-embedding-001"

_client = genai.Client(api_key=settings.GEMINI_API_KEY)


def embed_document(text: str) -> list[float]:
    return _embed(text, task_type="RETRIEVAL_DOCUMENT")


def embed_query(text: str) -> list[float]:
    return _embed(text, task_type="RETRIEVAL_QUERY")


def _embed(text: str, task_type: str) -> list[float]:
    response = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return response.embeddings[0].values