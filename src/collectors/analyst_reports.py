"""[1단계] 증권사 리포트 컨센서스 수집기.

수집 대상은 증권사 리포트의 정형 산출물이다.
  - 목표주가 (평균/최고/최저/중앙값)
  - 투자의견 분포 및 커버리지 애널리스트 수
  - 투자의견 변경 이력 (upgrade/downgrade)

취급 원칙 (docs/ARCHITECTURE.md 참조):
  외부 기관이 공표한 값을 가공 없이 그대로 전달한다.
  이 값들을 재료로 자체 점수/등급/종합 지수를 파생시키지 않는다.
  리포트 원문(PDF·본문)은 저작권상 자동 수집·저장하지 않으며,
  투자 포인트 요약은 NarrativeData 에 사람이 직접 입력한다.
"""

from __future__ import annotations

from datetime import date as date_type
from typing import Any, Iterable, List, Mapping, Optional

from src.collectors.base import (
    BatchResult,
    CollectorError,
    FieldSpec,
    TickerFactory,
    apply_specs,
    collect_many,
    default_ticker_factory,
    fetch_info,
    is_missing,
)
from src.types.stock import AnalystAction, AnalystRatingDistribution, AnalystReportData

SOURCE_LABEL = "yfinance (Yahoo Finance 애널리스트 컨센서스)"

# 목표주가·투자의견 컨센서스 매핑. 새 항목은 여기에 한 줄 추가.
FIELD_SPECS: List[FieldSpec] = [
    FieldSpec("target_price_mean", "targetMeanPrice"),
    FieldSpec("target_price_high", "targetHighPrice"),
    FieldSpec("target_price_low", "targetLowPrice"),
    FieldSpec("target_price_median", "targetMedianPrice"),
    FieldSpec("analyst_count", "numberOfAnalystOpinions", transform=int),
    FieldSpec("recommendation_mean", "recommendationMean"),
    FieldSpec("recommendation_key", "recommendationKey"),
]

# 투자의견 분포: 원천 컬럼명 -> 스키마 필드명
_DISTRIBUTION_COLUMNS = {
    "period": "period",
    "strongBuy": "strong_buy",
    "buy": "buy",
    "hold": "hold",
    "sell": "sell",
    "strongSell": "strong_sell",
}

# 투자의견 변경 이력: 원천 컬럼명 -> 스키마 필드명
_ACTION_COLUMNS = {
    "Firm": "firm",
    "FromGrade": "from_grade",
    "ToGrade": "to_grade",
    "Action": "action",
}


def _rows_from_frame(frame: Any) -> List[Mapping[str, Any]]:
    """DataFrame 또는 dict 리스트를 공통 형태(dict 리스트)로 정규화.

    원천이 pandas DataFrame이든 테스트용 dict 리스트든 동일하게 다루기 위한 어댑터.
    """
    if frame is None:
        return []
    if isinstance(frame, list):
        return [row for row in frame if isinstance(row, Mapping)]
    # pandas DataFrame 으로 간주
    to_dict = getattr(frame, "to_dict", None)
    if to_dict is None:
        return []
    if getattr(frame, "empty", False):
        return []
    # to_dict(orient="records")는 인덱스를 버린다. yfinance의 upgrades_downgrades는
    # 공표일(GradeDate)을 인덱스로 주므로, 이름 있는 인덱스는 컬럼으로 되살린 뒤 변환한다.
    reset_index = getattr(frame, "reset_index", None)
    index = getattr(frame, "index", None)
    if callable(reset_index) and index is not None and getattr(index, "name", None):
        try:
            frame = reset_index()
            to_dict = frame.to_dict
        except (TypeError, ValueError):
            pass
    try:
        return list(to_dict(orient="records"))
    except (TypeError, ValueError):
        return []


def _to_int(value: Any) -> Optional[int]:
    if is_missing(value):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_distribution(rows: List[Mapping[str, Any]]) -> Optional[AnalystRatingDistribution]:
    """투자의견 분포에서 최신 기준월(첫 행)만 취한다."""
    if not rows:
        return None
    row = rows[0]
    values: dict = {}
    for source_key, field_name in _DISTRIBUTION_COLUMNS.items():
        raw = row.get(source_key)
        if field_name == "period":
            values[field_name] = None if is_missing(raw) else str(raw)
        else:
            values[field_name] = _to_int(raw)
    if all(v is None for v in values.values()):
        return None
    return AnalystRatingDistribution(**values)


def _coerce_action_date(raw: Any) -> Optional[date_type]:
    """공표일을 date로 정규화. 형식을 알 수 없으면 추측하지 않고 None."""
    if is_missing(raw):
        return None
    if isinstance(raw, date_type) and not hasattr(raw, "hour"):
        return raw
    # datetime / pandas.Timestamp
    date_attr = getattr(raw, "date", None)
    if callable(date_attr):
        try:
            return date_attr()
        except (TypeError, ValueError):
            return None
    if isinstance(raw, str):
        try:
            return date_type.fromisoformat(raw[:10])
        except ValueError:
            return None
    return None


def _parse_actions(rows: List[Mapping[str, Any]], limit: int) -> List[AnalystAction]:
    """투자의견 변경 이력을 최신순으로 limit 건까지 변환."""
    actions: List[AnalystAction] = []
    for row in rows[:limit]:
        values = {
            field_name: (None if is_missing(row.get(src)) else str(row.get(src)))
            for src, field_name in _ACTION_COLUMNS.items()
        }
        # 공표일은 인덱스(GradeDate) 또는 동명 컬럼 어느 쪽으로도 올 수 있다.
        raw_date = row.get("GradeDate", row.get("Date", row.get("index")))
        values["action_date"] = _coerce_action_date(raw_date)
        if all(v is None for v in values.values()):
            continue
        actions.append(AnalystAction(**values))
    return actions


def collect_analyst_report(
    symbol: str,
    ticker_factory: TickerFactory = default_ticker_factory,
    action_limit: int = 10,
    today: Optional[date_type] = None,
) -> AnalystReportData:
    """단일 종목의 증권사 리포트 컨센서스 수집.

    info 조회 실패는 CollectorError로 올린다.
    반면 분포/변경이력은 부가 정보이므로, 조회에 실패해도 해당 항목만 비우고
    나머지 컨센서스는 살린다.
    """
    info = fetch_info(symbol, ticker_factory)
    values = apply_specs(info, FIELD_SPECS)

    ticker = ticker_factory(symbol)
    distribution = _parse_distribution(_safe_attr(ticker, "recommendations"))
    actions = _parse_actions(_safe_attr(ticker, "upgrades_downgrades"), action_limit)

    return AnalystReportData(
        symbol=symbol,
        rating_distribution=distribution,
        recent_actions=actions,
        source=SOURCE_LABEL,
        last_updated=today or date_type.today(),
        **values,
    )


def _safe_attr(ticker: Any, name: str) -> List[Mapping[str, Any]]:
    """부가 속성 조회. 실패 시 빈 목록으로 degrade (전체 수집을 막지 않는다)."""
    try:
        return _rows_from_frame(getattr(ticker, name, None))
    except Exception:
        return []


def collect_analyst_reports_many(
    symbols: Iterable[str],
    ticker_factory: TickerFactory = default_ticker_factory,
    action_limit: int = 10,
) -> BatchResult:
    """여러 종목 일괄 수집. 개별 실패는 BatchResult.errors 에 모인다."""
    return collect_many(
        symbols,
        lambda s: collect_analyst_report(s, ticker_factory, action_limit),
    )


__all__ = [
    "FIELD_SPECS",
    "SOURCE_LABEL",
    "CollectorError",
    "collect_analyst_report",
    "collect_analyst_reports_many",
]
