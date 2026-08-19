import streamlit as st

st.set_page_config(page_title="AI Stock Accumulation Dashboard", layout="wide")

st.title("📊 AI & Core Blue-Chip Accumulation Dashboard")
st.caption("Objective Data & Pullback Monitor | No Arbitrary Scoring")

tab1, tab2 = st.tabs(["1단계: 펀더멘털 & 내러티브", "2단계: 기술적 눌림목 타점"])

with tab1:
    st.subheader("기업 펀더멘털 및 핵심 내러티브")
    st.info("데이터 수집 모듈 연동 대기 중입니다.")

with tab2:
    st.subheader("기술적 지표 및 눌림목 현황")
    st.info("기술적 지표 연동 대기 중입니다.")
