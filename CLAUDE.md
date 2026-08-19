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
