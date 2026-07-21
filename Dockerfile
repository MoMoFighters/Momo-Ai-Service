# momo-ai 배포용 도커 이미지 구성

# Local venv 에서 쓰던 것과 같은 버전
# 하지만 slim 으로 이미지 용량을 최소화
FROM python:3.12-slim
WORKDIR /app

# Run pip install 의존성 레이어를 소스코드보다
# 먼저 복사해도 도커 캐시 재활용!!!
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 앱 코드, 정책 md 문서,
# ingest 스크립트까지 이미지에 포함
COPY app app
COPY docs docs
COPY scripts scripts

# 로컬에서 우리가 수동으로 쳤던 uvicorn app.main:app --host 0.0.0.0 --port 8001
# 을 그대로 컨테이너 기본 실행 명령으로 진행
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
