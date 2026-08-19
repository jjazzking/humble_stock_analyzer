"""[1단계] 펀더멘털 수집기.

새 펀더멘털 지표 추가 절차:
  1) src/types/stock.py 의 FundamentalData 에 필드 추가
  2) 아래 FIELD_SPECS 에 FieldSpec 한 줄 추가
"""

from __future__ import annotations

from typing import Iterable, List

from src.collectors.base import (
    BatchResult,
    FieldSpec,
    TickerFactory,
    collect_many,
    default_ticker_factory,
    fetch_info,
    apply_specs,
    to_percent,
)
from src.types.stock import FundamentalData

# 원천(yfinance info) 키 -> 스키마 필드 매핑 규칙
FIELD_SPECS: List[FieldSpec] = [
    FieldSpec("market_cap", "marketCap"),
    FieldSpec("pe_ratio", "trailingPE"),
    FieldSpec("forward_pe", "forwardPE"),
    FieldSpec(
        "revenue_growth_yoy",
        "revenueGrowth",
        transform=to_percent,
        note="원천은 소수 비율(0.12)로 제공하므로 퍼센트(12.0)로 변환",
    ),
    FieldSpec("free_cash_flow", "freeCashflow"),
]


def collect_fundamentals(
    symbol: str,
    ticker_factory: TickerFactory = default_ticker_factory,
) -> FundamentalData:
    """단일 종목의 펀더멘털 수집. 조회 실패 시 CollectorError."""
    info = fetch_info(symbol, ticker_factory)
    values = apply_specs(info, FIELD_SPECS)
    return FundamentalData(symbol=symbol, **values)


def collect_fundamentals_many(
    symbols: Iterable[str],
    ticker_factory: TickerFactory = default_ticker_factory,
) -> BatchResult:
    """여러 종목 일괄 수집. 개별 실패는 BatchResult.errors 에 모인다."""
    return collect_many(symbols, lambda s: collect_fundamentals(s, ticker_factory))
