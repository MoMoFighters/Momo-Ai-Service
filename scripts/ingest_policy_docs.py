import glob
import uuid

from app.service.chroma_client import get_collection
from app.service.embedding_service import embed_document

"""
docs/policies 밑 md 파일들을 섹션(## 단위)으로 쪼개서 Chroma에 적재하는 스크립트.
자바로 치면 초기 데이터 적재용 배치 잡(1회성 실행)과 같은 위치.
"""

POLICY_DIR = "docs/policies"


def load_chunks() -> list[str]:
    chunks = []
    for path in glob.glob(f"{POLICY_DIR}/*.md"):
        with open(path, encoding="utf-8") as f:
            content = f.read()

        sections = content.split("\n## ")
        file_chunks = []
        for i, section in enumerate(sections):
            text = section if i == 0 else "## " + section
            text = text.strip()
            if text:
                file_chunks.append(text)

        # 제목만 있는 첫 링크는 내용이 짧아 검색 상위권을 부당하게 차지하는
        # 문제가 있어서, 존재하면 바로 다음 청크와 합쳐서 하나의 링크로 만든다.
        if len(file_chunks) >= 2:
            file_chunks[1] = file_chunks[0] + "\n\n" + file_chunks[1]
            file_chunks = file_chunks[1:]

        chunks.extend(file_chunks)

    return chunks


def ingest():
    collection = get_collection()
    chunks = load_chunks()

    for chunk in chunks:
        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embed_document(chunk)],
            documents=[chunk],
        )

    print(f"{len(chunks)}개 청크 적재 완료")


if __name__ == "__main__":
    ingest()
