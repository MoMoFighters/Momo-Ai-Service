import chromadb

from app.config.settings import settings

"""
Chroma 서버(HTTP)에 연결하는 클라이언트.
자바로 치면 DataSource + JdbcTemplate 초기화하는 Config 클래스와 같은 역할.
"""

COLLECTION_NAME = "policy_faq"

_client = chromadb.HttpClient(
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT,
)


def get_collection():
    return _client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )