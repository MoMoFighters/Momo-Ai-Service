import pandas as pd

from app.service.chroma_client import get_collection
from app.service.embedding_service import embed_query

"""
RAG 검색 품질을 측정하는 벤치마크 스크립트.
고정된 질문 세트에 대해 "정답 청크"가 몇 등으로 검색되는지 확인해서
Hit@k(정답이 top_k 안에 들어왔는지)와 MRR(평균 역순위)을 계산한다.
"""

# 질문마다 "정답 청크"를 판별할 고유 문구(expected_keyword)를 미리 정의
TEST_CASES = [
    {"question": "환불은 언제까지 가능해?", "expected_keyword": "3일 이내"},
    {"question": "신고하면 얼마나 정지돼?", "expected_keyword": "1주일 정지"},
    {"question": "비밀번호를 수정하려면 어디로 가야해?", "expected_keyword": "현재 비밀번호를 반드시 입력"},
    {"question": "포인트는 어떻게 모아?", "expected_keyword": "챕터 하나를 완료할 때마다"},
    {"question": "건물은 어떻게 지어져?", "expected_keyword": "수강 신청에 성공하면"},
    {"question": "그룹 스터디방 몇 명까지 가능해?", "expected_keyword": "최대 4명"},
    {"question": "멤버십은 어떻게 결제해?", "expected_keyword": "BASIC"},
    {"question": "회원가입하려면 뭐가 필요해?", "expected_keyword": "이메일 인증"},
]

TOP_K = 8


# 검색된 문서 리스트에서 정답 문구가 몇 번째에 있는지 찾음 (1등부터 시작, 없으면 None)
def rank_of_expected(documents: list[str], expected_keyword: str) -> int | None:
    for i, doc in enumerate(documents, start=1):
        if expected_keyword in doc:
            return i
    return None


def run_benchmark():
    collection = get_collection()
    rows = []

    # 각 질문 8개 + 각 질문의 정답 청크를 식별할 고유 문구
    for case in TEST_CASES:
        query_vector = embed_query(case["question"])
        result = collection.query(
            query_embeddings=[query_vector],
            n_results=TOP_K,
            include=["documents"],
        )
        documents = result["documents"][0]
        # 검색 결과 안에서 정답 문구가 몇 번째 순위에 있는지 찾음
        rank = rank_of_expected(documents, case["expected_keyword"])

        rows.append({
            "질문": case["question"],
            "정답 순위": rank if rank else "못 찾음",
            f"Hit@{TOP_K}": rank is not None,
            "역순위(1/rank)": round(1 / rank, 3) if rank else 0.0,
        })

    df = pd.DataFrame(rows)
    hit_rate = df[f"Hit@{TOP_K}"].mean()
    mrr = df["역순위(1/rank)"].mean()

    print(df.to_string(index=False))
    print()
    print(f"Hit@{TOP_K}: {hit_rate:.1%}")
    print(f"MRR: {mrr:.3f}")

# run_benchmark() - 질문마다 검색 돌려서 검색 순위 기록
# 판다스 표로 정리 후 Hit@8/MRR 집계
if __name__ == "__main__":
    run_benchmark()