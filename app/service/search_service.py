from app.service.chroma_client import get_collection
from app.service.embedding_service import embed_query

"""
질문 -> 벡터 -> Chroma 유사도 검색 -> 관련 문서 텍스트 리스트.
자바로 치면 Repository가 DB 조회해서 결과 매핑해주는 것과 같은 위치.
"""


def search_policy(query: str, top_k: int = 5) -> list[str]:
    query_vector = embed_query(query)
    collection = get_collection()

    result = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
    )

    return result["documents"][0]