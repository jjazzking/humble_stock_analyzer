"""실데이터 수집 점검 스크립트.

네트워크가 열린 환경에서 1회 실행해 원천 키 매핑이 실제로 맞는지 확인한다.
실행: python -m src.collectors.smoke [SYMBOL ...]

값이 None으로 나오면 두 경우를 구분해서 봐야 한다.
  - 원천에 그 항목이 원래 없음  -> 정상
  - 원천 키 이름이 바뀜          -> FIELD_SPECS 수정 필요
"""

from __future__ import annotations

import sys
from typing import List

from src.collectors.analyst_reports import collect_analyst_reports_many
from src.collectors.fundamentals import collect_fundamentals_many
from src.collectors.watchlist import load_symbols


def _fmt(value: object) -> str:
    return "N/A" if value is None else str(value)


def main(argv: List[str]) -> int:
    symbols = argv[1:] or load_symbols()
    print(f"대상 종목: {', '.join(symbols)}\n")

    print("=" * 60)
    print("[1] 펀더멘털")
    print("=" * 60)
    fundamentals = collect_fundamentals_many(symbols)
    for record in fundamentals.records:
        print(
            f"{record.symbol:6s} 시총={_fmt(record.market_cap):>18s} "
            f"PER={_fmt(record.pe_ratio):>8s} "
            f"FwdPER={_fmt(record.forward_pe):>8s} "
            f"매출성장률={_fmt(record.revenue_growth_yoy):>8s}%"
        )

    print()
    print("=" * 60)
    print("[2] 증권사 리포트 컨센서스")
    print("=" * 60)
    reports = collect_analyst_reports_many(symbols)
    for report in reports.records:
        print(
            f"{report.symbol:6s} 목표주가 평균={_fmt(report.target_price_mean):>8s} "
            f"(최저 {_fmt(report.target_price_low)} ~ 최고 {_fmt(report.target_price_high)}) "
            f"커버리지={_fmt(report.analyst_count)}명 "
            f"의견={_fmt(report.recommendation_key)}"
        )
        dist = report.rating_distribution
        if dist is not None:
            print(
                f"       투자의견 분포[{_fmt(dist.period)}] "
                f"적극매수 {_fmt(dist.strong_buy)} / 매수 {_fmt(dist.buy)} / "
                f"중립 {_fmt(dist.hold)} / 매도 {_fmt(dist.sell)} / "
                f"적극매도 {_fmt(dist.strong_sell)}"
            )
        for action in report.recent_actions[:3]:
            print(
                f"       {_fmt(action.action_date)} {_fmt(action.firm)}: "
                f"{_fmt(action.from_grade)} -> {_fmt(action.to_grade)} ({_fmt(action.action)})"
            )

    errors = {**fundamentals.errors, **reports.errors}
    if errors:
        print("\n[수집 실패]")
        for symbol, message in errors.items():
            print(f"  {symbol}: {message}")
        return 1

    print("\n모든 종목 수집 성공")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
