"""테스트 공용 페이크 원천.

Yahoo Finance 실호출 없이 수집기 로직을 검증하기 위한 가짜 Ticker.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional


class FakeTicker:
    """yfinance.Ticker 대역."""

    def __init__(
        self,
        info: Optional[Mapping[str, Any]] = None,
        recommendations: Any = None,
        upgrades_downgrades: Any = None,
        raise_on_info: Optional[Exception] = None,
    ) -> None:
        self._info = info if info is not None else {}
        self.recommendations = recommendations
        self.upgrades_downgrades = upgrades_downgrades
        self._raise_on_info = raise_on_info

    @property
    def info(self) -> Mapping[str, Any]:
        if self._raise_on_info is not None:
            raise self._raise_on_info
        return self._info


def factory_for(**by_symbol: FakeTicker):
    """심볼별 FakeTicker 를 돌려주는 ticker_factory 를 만든다."""

    def _factory(symbol: str) -> FakeTicker:
        if symbol not in by_symbol:
            return FakeTicker(info={})
        return by_symbol[symbol]

    return _factory


NVDA_INFO = {
    "marketCap": 3_400_000_000_000,
    "trailingPE": 52.4,
    "forwardPE": 31.2,
    "revenueGrowth": 0.1224,
    "freeCashflow": 60_100_000_000,
    "targetMeanPrice": 210.5,
    "targetHighPrice": 275.0,
    "targetLowPrice": 120.0,
    "targetMedianPrice": 215.0,
    "numberOfAnalystOpinions": 62,
    "recommendationMean": 1.34,
    "recommendationKey": "strong_buy",
}

NVDA_RECOMMENDATIONS = [
    {"period": "0m", "strongBuy": 40, "buy": 18, "hold": 4, "sell": 0, "strongSell": 0},
    {"period": "-1m", "strongBuy": 39, "buy": 17, "hold": 5, "sell": 0, "strongSell": 0},
]

NVDA_UPGRADES = [
    {
        "GradeDate": "2026-08-12",
        "Firm": "Morgan Stanley",
        "FromGrade": "Equal-Weight",
        "ToGrade": "Overweight",
        "Action": "up",
    },
    {
        "GradeDate": "2026-07-30",
        "Firm": "Goldman Sachs",
        "FromGrade": "Buy",
        "ToGrade": "Buy",
        "Action": "main",
    },
]
