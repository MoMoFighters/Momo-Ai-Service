from app.service.chroma_client import get_collection
from app.service.embedding_service import embed_query

"""
질문 -> 벡터 -> Chroma 유사도 검색 -> 관련 문서 텍스트 리스트.
자바로 치면 Repository가 DB 조회해서 결과 매핑해주는 것과 같은 위치.
"""

SIMILARITY_THRESHOLD = 0.67


def search_policy(query: str, top_k: int = 5) -> list[str]:
    query_vector = embed_query(query)
    collection = get_collection()

    result = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        # 기존에는 문서 텍스트만 받았지만, 걸러내기 위해서 거리값도 같이 받아야함.
        include=["documents", "distances"],
    )

    # Chroma DB 응답이 쿼리 1개 기준 리스트 안에 리스트로 [0] 으로 꺼냄
    documents = result["documents"][0]
    distances = result["distances"][0]

    return [
        doc
        for doc, distance in zip(documents, distances)
        if (1 - distance) >= SIMILARITY_THRESHOLD
    ]