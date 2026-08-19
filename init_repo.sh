#!/bin/bash
# AI Stock Accumulation Dashboard - Repository Initializer
# Run this in an empty directory or cloned GitHub repo.

# 1. Directories
mkdir -p docs
mkdir -p config
mkdir -p src/collectors
mkdir -p src/indicators
mkdir -p src/dashboard
mkdir -p src/types
mkdir -p data/raw
mkdir -p data/processed
mkdir -p tests

# 2. .gitignore
cat << 'EOF' > .gitignore
# Python / Virtualenv
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
.env.local

# Data storage (keep raw/processed local, only schema in git)
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# IDE & OS
.DS_Store
.vscode/
.idea/
EOF

touch data/raw/.gitkeep
touch data/processed/.gitkeep

# 3. CLAUDE.md (Core Rules & Token Saver)
cat << 'EOF' > CLAUDE.md
# AI Stock Accumulation Dashboard Rules

## Project Objective
- Build a clear, unopinionated dashboard for accumulating solid AI & tech stocks during pullbacks (눌림목).
- Strict separation: 
  - Phase 1: Objective Fundamental & Narrative collection
  - Phase 2: Simple Technical pullback metrics

## Absolute Constraints (Strict Guardrails)
1. **NO Arbitrary Scoring / Subjective Rating:** NEVER create proprietary "scores" (e.g. 78/100, "Bullish Rank", "AI Grade"). Output pure, verified raw metrics and mathematical technical indicators only.
2. **Data Integrity Over Everything:** If a data point is missing or unverified, mark as `null` or `N/A`. Do not guess or interpolate.
3. **Extensibility First:** Metrics/indicators are modular. Placeholders are designed for future user additions.
4. **Token Optimization:** Always generate clean, modular code targeting specific files in `src/`. Do not re-explain architecture.

## Tech Stack
- Language: Python 3.11+
- Data: `pandas`, `yfinance` (or financial APIs), `pydantic` (schema validation)
- UI/Dashboard: `streamlit` (lightweight, zero boilerplate)
- Tests: `pytest`
EOF

# 4. docs/ARCHITECTURE.md
cat << 'EOF' > docs/ARCHITECTURE.md
# Architecture & Data Flow

```text
[Data Sources (APIs / yfinance / Edgar)]
                 │
                 ▼
     [src/collectors/] ──► Validates via [src/types/]
                 │
                 ▼
     [src/indicators/] ──► Computes raw technical/fundamental metrics (NO scoring)
                 │
                 ▼
     [src/dashboard/]  ──► Pure data presentation in Streamlit table/charts
```

### Module Responsibilities
- `src/types/`: Pydantic models enforcing strict schemas and data integrity.
- `src/collectors/`: Functions to fetch historical price data, financial statements, and news/narratives.
- `src/indicators/`: Modular calculation functions (e.g., RSI, Moving Averages, Drawdown, Valuation multiples).
- `src/dashboard/`: Streamlit presentation layer (filters, tables, metric cards).
EOF

# 5. docs/TODO.md
cat << 'EOF' > docs/TODO.md
# Development Roadmap

- [ ] **Phase 0: Environment & Watchlist Setup**
  - [ ] Setup `config/watchlist.yaml` with target AI & blue-chip tickers
  - [ ] Define core data contracts in `src/types/stock.py`

- [ ] **Phase 1: Fundamental & Narrative Pipeline (1단계)**
  - [ ] Build fundamental collector (`src/collectors/fundamentals.py`)
  - [ ] Build narrative/filings collector (`src/collectors/narrative.py`)
  - [ ] Verify data integrity tests in `tests/test_collectors.py`

- [ ] **Phase 2: Technical Pullback Metrics (2단계)**
  - [ ] Build simple pullback indicators (`src/indicators/pullback.py`)
    - 20/50/200-day SMA distance (%)
    - 52-Week High Drawdown (%)
    - Basic RSI / Support levels
  - [ ] Verify indicator calculations in `tests/test_indicators.py`

- [ ] **Phase 3: Streamlit Pure Dashboard (3단계)**
  - [ ] Tab 1: Fundamentals & Narrative View
  - [ ] Tab 2: Pullback & Technical Level View
  - [ ] Raw Data Export (CSV/Parquet)
EOF

# 6. config/watchlist.yaml
cat << 'EOF' > config/watchlist.yaml
# Target Watchlist: AI Infra, Semi, Cloud & Core Blue-chips
tickers:
  - symbol: NVDA
    name: NVIDIA
    category: AI Chips / Hardware
  - symbol: MSFT
    name: Microsoft
    category: Cloud / Software
  - symbol: GOOGL
    name: Alphabet
    category: Model / Platform
  - symbol: TSM
    name: TSMC
    category: Foundry
  - symbol: ASML
    name: ASML
    category: Equipment
EOF

# 7. src/types/stock.py (Data Contract Skeleton)
cat << 'EOF' > src/types/stock.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date

class FundamentalData(BaseModel):
    symbol: str
    market_cap: Optional[float] = Field(None, description="Market Cap in USD")
    pe_ratio: Optional[float] = Field(None, description="Trailing P/E")
    forward_pe: Optional[float] = Field(None, description="Forward P/E")
    revenue_growth_yoy: Optional[float] = Field(None, description="YoY Revenue Growth %")
    free_cash_flow: Optional[float] = Field(None, description="Latest FCF")
    # Future metrics can be added here without breaking existing code

class NarrativeData(BaseModel):
    symbol: str
    key_catalysts: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    last_updated: Optional[date] = None

class TechnicalData(BaseModel):
    symbol: str
    current_price: float
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    distance_sma_50_pct: Optional[float] = Field(None, description="Distance from 50 SMA (%)")
    high_52w_drawdown_pct: Optional[float] = Field(None, description="Drawdown from 52w High (%)")
    rsi_14: Optional[float] = None
    # Future technical metrics can be added here

class StockRecord(BaseModel):
    symbol: str
    fundamentals: FundamentalData
    narrative: NarrativeData
    technicals: TechnicalData
EOF

# 8. src/dashboard/app.py (Streamlit Skeleton)
cat << 'EOF' > src/dashboard/app.py
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
EOF

# 9. requirements.txt
cat << 'EOF' > requirements.txt
pandas>=2.0.0
yfinance>=0.2.30
pydantic>=2.0.0
streamlit>=1.30.0
pyyaml>=6.0
pytest>=8.0.0
EOF

echo "Repository skeleton successfully created."
