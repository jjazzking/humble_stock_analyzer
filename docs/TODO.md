# 개발 체크리스트 및 로드맵

- [x] **0단계: 환경 구성 및 감시 종목군 설정**
  - [x] `config/watchlist.yaml`에 대상 AI 및 빅테크 종목 티커 등록
  - [x] `src/types/stock.py` 기본 데이터 스키마 확정
  - [x] `src/` 패키지화 및 import 경로 정리 (pyproject.toml)

- [ ] **1단계: 펀더멘털 & 증권사 리포트 수집 파이프라인 (기본 분석)**
  - [x] 수집기 공통 기반 작성 (`src/collectors/base.py`)
    - FieldSpec 매핑, 결측 판정, 수집 실패/값 부재 구분, 배치 오류 격리
  - [x] watchlist 로더 작성 (`src/collectors/watchlist.py`)
  - [x] 펀더멘털 수집기 작성 (`src/collectors/fundamentals.py`)
  - [x] 증권사 리포트 컨센서스 수집기 작성 (`src/collectors/analyst_reports.py`)
    - 목표주가(평균/최고/최저/중앙), 투자의견 분포, 커버리지 수, 의견 변경 이력
  - [x] 데이터 수집 정합성 테스트 (`tests/test_collectors.py`)
  - [ ] **실데이터 검증** — 개발 환경 네트워크 정책으로 Yahoo Finance 차단 상태.
        로컬에서 `python -m src.collectors.smoke` 등으로 실호출 1회 확인 필요
  - [ ] 실적 추정치(EPS/매출 컨센서스) 수집 항목 추가
  - [ ] 내러티브 수집기 작성 (`src/collectors/narrative.py`)
        ※ 리포트 원문은 저작권상 자동 수집하지 않고 수기 입력

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
