#!/bin/bash
# AI 주식 눌림목 분할매수 대시보드 - 저장소 초기화 스크립트
# 빈 폴더 또는 로컬 깃 저장소 폴더에서 실행하세요.

# 1. 디렉터리 생성
mkdir -p docs
mkdir -p config
mkdir -p src/collectors
mkdir -p src/indicators
mkdir -p src/dashboard
mkdir -p src/types
mkdir -p data/raw
mkdir -p data/processed
mkdir -p tests

# 2. .gitignore 생성
cat << 'EOF' > .gitignore
# 파이썬 가상환경 및 캐시
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
.env.local

# 로컬 데이터 (스키마만 깃에 남기고 원본/가공 데이터는 제외)
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# IDE 및 OS 설정 파일
.DS_Store
.vscode/
.idea/
EOF

touch data/raw/.gitkeep
touch data/processed/.gitkeep

# 3. CLAUDE.md (AI 핵심 행동 지침 및 토큰 절약 규칙)
cat << 'EOF' > CLAUDE.md
# AI 주식 눌림목 분할매수 대시보드 개발 규칙

## 프로젝트 목표
- AI 시대 수혜주 및 우량 기술주의 객관적 지표를 기반으로, 단기 눌림목(조정 구간)에서 분할 매수할 수 있도록 돕는 대시보드 구축.
- 단계별 명확한 분리:
  - 1단계: 객관적 펀더멘털 및 투자 내러티브 수집
  - 2단계: 단순 기술적 지표 기반 눌림목 모니터링

## 절대 원칙 및 금지 사항 (Strict Constraints)
1. **임의 점수 산출(Scoring) 및 등급 부여 절대 금지:**
   - "매수 점수 80점", "A등급", "자체 상승지수" 같은 주관적이거나 가공된 점수를 절대 만들지 않는다.
   - 오직 검증된 원천 수치(재무 데이터)와 수학적 기술 지표(이격도, 고점 대비 낙폭 등)만 정직하게 출력한다.
2. **데이터 정합성(무결성) 최우선:**
   - 데이터가 누락되었거나 확인되지 않은 경우 추정해서 채우지 말고 `null` 또는 `N/A`로 명확히 표시한다.
3. **지표 확장성 보장:**
   - 지표나 펀더멘털 항목은 사용자가 나중에 얼마든지 추가할 수 있도록 모듈식 함수 및 확장 가능한 스키마 구조로 작성한다.
4. **토큰 절약 최적화:**
   - 장황한 개념 설명이나 아키텍처 재설명을 생략하고, `src/` 내의 특정 대상 파일에 필요한 완성형 코드만 바로 작성한다.

## 기술 스택
- 언어: Python 3.11+
- 데이터 수집/처리: `pandas`, `yfinance`, `pydantic` (데이터 스키마 검증)
- 대시보드 UI: `streamlit`
- 테스트: `pytest`
EOF

# 4. README.md (프로젝트 소개 및 안내서)
cat << 'EOF' > README.md
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
source .venv/bin/activate  # Windows 환경: .venv\Scriptsctivate
pip install -r requirements.txt
```

### 2. 대시보드 실행
```bash
streamlit run src/dashboard/app.py
```
EOF

# 5. docs/ARCHITECTURE.md (아키텍처 문서)
cat << 'EOF' > docs/ARCHITECTURE.md
# 아키텍처 및 데이터 흐름도

```text
[데이터 원천 (yfinance / 공시 / 뉴스 API)]
                    │
                    ▼
     [src/collectors/] (데이터 수집) ──► [src/types/] (스키마 검증 및 정합성 보장)
                    │
                    ▼
     [src/indicators/] (지표 계산)   ──► 순수 기술적/기본적 지표 계산 (점수화 절대 금지)
                    │
                    ▼
     [src/dashboard/]  (대시보드 표출) ──► Streamlit 기반 표/차트로 정직하게 시각화
```

### 모듈별 역할 및 책임
- `src/types/`: 데이터 무결성과 정합성을 강제하는 Pydantic 모델 정의.
- `src/collectors/`: 주가 시세, 재무제표 수치, 기업 내러티브 등을 수집하는 모듈.
- `src/indicators/`: 이동평균선 이격도, 52주 고점 대비 낙폭(MDD), RSI 등 순수 수학적 지표 계산.
- `src/dashboard/`: 필터링, 표 조회, 핵심 지표 카드 등 UI 화면 표출.
EOF

# 6. docs/TODO.md (개발 로드맵)
cat << 'EOF' > docs/TODO.md
# 개발 체크리스트 및 로드맵

- [ ] **0단계: 환경 구성 및 감시 종목군 설정**
  - [ ] `config/watchlist.yaml`에 대상 AI 및 빅테크 종목 티커 등록
  - [ ] `src/types/stock.py` 기본 데이터 스키마 확정

- [ ] **1단계: 펀더멘털 & 내러티브 수집 파이프라인 (기본 분석)**
  - [ ] 펀더멘털 수집기 작성 (`src/collectors/fundamentals.py`)
  - [ ] 내러티브/공시 수집기 작성 (`src/collectors/narrative.py`)
  - [ ] 데이터 수집 정합성 테스트 (`tests/test_collectors.py`)

- [ ] **2단계: 단순 기술적 눌림목 타점 계산 (타점 분석)**
  - [ ] 눌림목 지표 계산기 작성 (`src/indicators/pullback.py`)
    - 20일 / 50일 / 200일 이동평균선 이격도 (%)
    - 52주 신고가 대비 하락률 (Drawdown %)
    - 기본 RSI 및 주요 지지 구간
  - [ ] 지표 계산 정합성 테스트 (`tests/test_indicators.py`)

- [ ] **3단계: Streamlit 대시보드 표출 (화면 완성)**
  - [ ] 탭 1: 펀더멘털 및 내러티브 종합 뷰
  - [ ] 탭 2: 기술적 눌림목 타점 모니터링 뷰
  - [ ] 원본 데이터 CSV 다운로드 기능
EOF

# 7. config/watchlist.yaml (감시 종목군)
cat << 'EOF' > config/watchlist.yaml
# 모니터링 대상 종목군: AI 하드웨어, 클라우드, 파운드리 등 핵심 우량주
tickers:
  - symbol: NVDA
    name: 엔비디아 (NVIDIA)
    category: AI 반도체 / 하드웨어
  - symbol: MSFT
    name: 마이크로소프트 (Microsoft)
    category: 클라우드 / 소프트웨어
  - symbol: GOOGL
    name: 알파벳 (Alphabet)
    category: AI 모델 / 플랫폼
  - symbol: TSM
    name: TSMC
    category: 파운드리
  - symbol: ASML
    name: ASML
    category: 반도체 장비
EOF

# 8. src/types/stock.py (데이터 스키마)
cat << 'EOF' > src/types/stock.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class FundamentalData(BaseModel):
    """기업 펀더멘털 데이터 규격"""
    symbol: str
    market_cap: Optional[float] = Field(None, description="시가총액 (USD)")
    pe_ratio: Optional[float] = Field(None, description="트레일링 P/E (과거 PER)")
    forward_pe: Optional[float] = Field(None, description="포워드 P/E (선행 PER)")
    revenue_growth_yoy: Optional[float] = Field(None, description="전년 대비 매출 성장률 (%)")
    free_cash_flow: Optional[float] = Field(None, description="최근 잉여현금흐름 (FCF)")
    # 향후 원하는 펀더멘털 지표(ROE, 영업이익률 등)를 이곳에 손쉽게 추가 가능

class NarrativeData(BaseModel):
    """기업 투자 내러티브 및 핵심 이슈 규격"""
    symbol: str
    business_summary: Optional[str] = Field(None, description="주요 사업 및 AI 관련성 요약")
    key_catalysts: List[str] = Field(default_factory=list, description="주요 상승 모멘텀 / 촉매")
    risk_factors: List[str] = Field(default_factory=list, description="주요 리스크 요인")
    last_updated: Optional[date] = Field(None, description="최종 업데이트 일자")

class TechnicalData(BaseModel):
    """기술적 지표 및 눌림목 데이터 규격 (점수화 없는 순수 수학적 지표)"""
    symbol: str
    current_price: float = Field(..., description="현재 주가")
    sma_50: Optional[float] = Field(None, description="50일 단순이동평균")
    sma_200: Optional[float] = Field(None, description="200일 단순이동평균")
    distance_sma_50_pct: Optional[float] = Field(None, description="50일 이평선 대비 이격도 (%)")
    high_52w_drawdown_pct: Optional[float] = Field(None, description="52주 최고가 대비 하락률 (%)")
    rsi_14: Optional[float] = Field(None, description="14일 기준 RSI")
    # 향후 원하는 기술적 지표(볼린저 밴드, 거래량 등)를 이곳에 손쉽게 추가 가능

class StockRecord(BaseModel):
    """개별 종목 종합 레코드"""
    symbol: str
    name: Optional[str] = None
    fundamentals: FundamentalData
    narrative: NarrativeData
    technicals: TechnicalData
EOF

# 9. src/dashboard/app.py (대시보드 UI)
cat << 'EOF' > src/dashboard/app.py
import streamlit as st

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
EOF

# 10. requirements.txt (의존성 패키지)
cat << 'EOF' > requirements.txt
pandas>=2.0.0
yfinance>=0.2.30
pydantic>=2.0.0
streamlit>=1.30.0
pyyaml>=6.0
pytest>=8.0.0
EOF

echo "한국어 주석 및 문서가 포함된 초기 저장소 구조 생성이 완료되었습니다."
