import sys
from pathlib import Path

# streamlit run 실행 시 sys.path에는 이 스크립트의 폴더(src/dashboard)만 등록되므로
# 프로젝트 루트를 직접 추가한다. src/ 자체가 아닌 루트를 추가해야 src.types가
# 표준 라이브러리 types 모듈을 가리는 문제를 피할 수 있다.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st  # noqa: E402

st.set_page_config(page_title="AI 우량주 눌림목 대시보드", layout="wide")

st.title("📊 AI & 핵심 우량주 눌림목 분할매수 모니터")
st.caption("객관적 원천 데이터 및 단순 기술적 지표 모니터링 | 임의 점수화 배제")

tab1, tab2 = st.tabs(["1단계: 펀더멘털 & 내러티브", "2단계: 기술적 눌림목 타점"])

with tab1:
    st.subheader("기업별 펀더멘털 및 투자 내러티브")
    st.info("데이터 수집 모듈(src/collectors/) 연동 대기 중입니다.")

with tab2:
    st.subheader("기술적 지표 및 눌림목 현황")
    st.info("지표 계산 모듈(src/indicators/) 연동 대기 중입니다.")
