"""
FastAPI 앱의 진입점
자바의 Application.java 와 같은 역할
"""
from fastapi import FastAPI

from app.router import embed_router, search_router

app = FastAPI(title="Momo AI Service")

app.include_router(embed_router.router)
app.include_router(search_router.router)


# 서버 떠 있는지 확인용 (자바로 치면 헬스체크 엔드포인트)
@app.get("/health")
def health_check():
    return {"status": "ok"}