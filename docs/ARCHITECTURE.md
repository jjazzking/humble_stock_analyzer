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
