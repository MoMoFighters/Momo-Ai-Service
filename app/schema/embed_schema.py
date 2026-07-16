from pydantic import BaseModel

"""
/embed API 요청/응답 형태 정의 - Java 에서 ChatbotQuestionRequest/Response 같은 DTO 역할
"""

class EmbedRequest(BaseModel):
    text: str


class EmbedResponse(BaseModel):
    embedding: list[float]