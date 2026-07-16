from pydantic import BaseModel

"""
/search API 의 요청/응답 형태 정의 - 위와 동일한 역할, 대상만 검색으로 다룸
"""

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResponse(BaseModel):
    results: list[str]