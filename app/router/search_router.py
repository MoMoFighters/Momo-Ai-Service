from fastapi import APIRouter

from app.schema.search_schema import SearchRequest, SearchResponse

"""
백터 DB(Chroma)에서 유사한 문서를 찾아주는 /search 엔드포인트 골격이다.
"""

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search(request: SearchRequest):
    # TODO: Chroma 벡터 검색 연동 (다음 작업)
    return SearchResponse(results=[])