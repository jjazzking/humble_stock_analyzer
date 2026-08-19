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
