# 📊 AI & 핵심 우량주 눌림목 분할매수 대시보드
> AI 시대 수혜주 및 우량 기술주의 객관적인 펀더멘털과 단기 눌림목 타점을 모니터링하는 데이터 대시보드

---

## 🎯 프로젝트 개요
본 프로젝트는 주관적인 해석이나 불필요한 과최적화 지표를 배제하고, **신뢰성 높은 원천 데이터**와 **단순한 기술적 지표**만을 활용해 장기 성장 우량주의 단기 조정(눌림목) 타점을 모니터링하기 위해 구축되었습니다.

- **1단계 (기본 분석):** 핵심 펀더멘털 지표 및 기업 투자 내러티브 수집·정리
- **2단계 (타점 분석):** 이동평균선 이격도, 고점 대비 낙폭, 기본 모멘텀 기반 눌림목 추적

---

## ⚖️ 핵심 원칙 (Core Rules)
1. **임의적 점수 산출(Scoring) 절대 금지**
   - "매수 점수 85점", "투자 등급 A+" 등 블랙박스형 자체 점수화 로직을 일절 배제하고, 검증된 원천 수치와 수학적 지표만 표시합니다.
2. **데이터 정합성 최우선**
   - 데이터 누락이나 오류가 있을 경우 자의적으로 추정치를 채우지 않고 명확히 `null`/`N/A`로 표기합니다.
3. **지표 확장성 보장**
   - 새로운 펀더멘털/기술적 지표가 떠오를 때마다 코드 구조를 뜯어고치지 않고 모듈 단위로 손쉽게 추가할 수 있도록 설계합니다.

---

## 🏗️ 디렉터리 구조

```text
ai-stock-dashboard/
├── CLAUDE.md                 # AI 어시스턴트용 규칙 및 제약사항
├── README.md                 # 프로젝트 소개 및 안내서
├── requirements.txt          # 의존성 라이브러리 목록
├── pyproject.toml            # pytest import 경로 설정
├── config/
│   └── watchlist.yaml        # 모니터링 대상 종목(Watchlist) 설정
├── docs/
│   ├── ARCHITECTURE.md       # 아키텍처 및 데이터 흐름도
│   └── TODO.md               # 단계별 개발 진행 로드맵
├── src/
│   ├── types/
│   │   └── stock.py          # 데이터 스키마 정의 (Pydantic 모델)
│   ├── collectors/           # [1단계] 펀더멘털 및 내러티브 데이터 수집기
│   ├── indicators/           # [2단계] 기술적 지표 및 눌림목 계산 모듈
│   └── dashboard/
│       └── app.py            # Streamlit 대시보드 UI
└── tests/                    # 데이터 무결성 검증 테스트
```

---

## 🚀 빠른 시작

### 1. 가상환경 설정 및 패키지 설치
```bash
python -m venv .venv
source .venv/bin/activate  # Windows 환경: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 대시보드 실행
```bash
streamlit run src/dashboard/app.py
```
