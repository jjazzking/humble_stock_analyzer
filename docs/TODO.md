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
