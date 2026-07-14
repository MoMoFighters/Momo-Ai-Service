from pydantic_settings import BaseSettings, SettingsConfigDict
"""
.env 에 있는 값들을 파이썬 객체로 읽어들이는 설정 로더
자바 : application.yaml 을 읽어서 @ConfigurationProperties 로 매핑하는 것과 동일한 개념
"""

class Settings(BaseSettings):
    # .env 파일에서 값을 읽어온다는 설정
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    GEMINI_API_KEY: str          # 필수값 — 없으면 앱 시작할 때 바로 에러
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000


# 앱 전체에서 이 객체 하나만 가져다 쓰면 됨 (싱글턴처럼 사용)
settings = Settings()