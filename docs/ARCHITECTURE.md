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
