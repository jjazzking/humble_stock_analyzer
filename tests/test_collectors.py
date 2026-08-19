"""수집기 정합성 테스트 (네트워크 미사용)."""

from __future__ import annotations

from datetime import date

import pytest

from src.collectors.analyst_reports import collect_analyst_report, collect_analyst_reports_many
from src.collectors.base import CollectorError, is_missing, to_percent
from src.collectors.fundamentals import collect_fundamentals, collect_fundamentals_many
from src.collectors.watchlist import load_symbols, load_watchlist
from tests.conftest import (
    NVDA_INFO,
    NVDA_RECOMMENDATIONS,
    NVDA_UPGRADES,
    FakeTicker,
    factory_for,
)


# --- 결측 판정 -------------------------------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        (None, True), (float("nan"), True), ("", True), ("   ", True),
        (float("inf"), True), (0, False), (0.0, False), ("NVDA", False),
    ],
)
def test_is_missing(value, expected):
    assert is_missing(value) is expected


def test_zero_is_not_missing():
    """0 은 유효한 값이다. 결측으로 오인해 N/A 처리하면 안 된다."""
    assert is_missing(0) is False


# --- 펀더멘털 --------------------------------------------------------------

def test_fundamentals_maps_source_values():
    factory = factory_for(NVDA=FakeTicker(info=NVDA_INFO))
    data = collect_fundamentals("NVDA", factory)

    assert data.symbol == "NVDA"
    assert data.market_cap == 3_400_000_000_000
    assert data.pe_ratio == 52.4
    assert data.forward_pe == 31.2
    assert data.free_cash_flow == 60_100_000_000


def test_revenue_growth_converted_to_percent():
    """원천은 소수 비율, 스키마는 퍼센트."""
    factory = factory_for(NVDA=FakeTicker(info=NVDA_INFO))
    assert collect_fundamentals("NVDA", factory).revenue_growth_yoy == to_percent(0.1224)
    assert collect_fundamentals("NVDA", factory).revenue_growth_yoy == 12.24


def test_missing_fields_become_none_not_estimated():
    """원천에 없는 값은 추정하지 않고 None."""
    factory = factory_for(X=FakeTicker(info={"marketCap": 100}))
    data = collect_fundamentals("X", factory)

    assert data.market_cap == 100
    assert data.pe_ratio is None
    assert data.forward_pe is None
    assert data.revenue_growth_yoy is None
    assert data.free_cash_flow is None


def test_nan_from_source_becomes_none():
    factory = factory_for(X=FakeTicker(info={"trailingPE": float("nan")}))
    assert collect_fundamentals("X", factory).pe_ratio is None


def test_uncastable_value_becomes_none():
    """변환 실패 시 추측해 채우지 않는다."""
    factory = factory_for(X=FakeTicker(info={"revenueGrowth": "해당없음"}))
    assert collect_fundamentals("X", factory).revenue_growth_yoy is None


# --- 수집 실패와 값 부재의 구분 ---------------------------------------------

def test_fetch_failure_raises_instead_of_silent_na():
    """네트워크 장애가 N/A로 위장되면 안 된다."""
    factory = factory_for(X=FakeTicker(raise_on_info=ConnectionError("tunnel 403")))
    with pytest.raises(CollectorError) as exc:
        collect_fundamentals("X", factory)
    assert "원천 조회 실패" in exc.value.message


def test_empty_response_raises():
    factory = factory_for(X=FakeTicker(info={}))
    with pytest.raises(CollectorError):
        collect_fundamentals("X", factory)


def test_batch_isolates_failures():
    """한 종목 실패가 배치 전체를 죽이지 않는다."""
    factory = factory_for(
        NVDA=FakeTicker(info=NVDA_INFO),
        BAD=FakeTicker(raise_on_info=ConnectionError("boom")),
    )
    result = collect_fundamentals_many(["NVDA", "BAD"], factory)

    assert [r.symbol for r in result.records] == ["NVDA"]
    assert "BAD" in result.errors
    assert result.ok is False


# --- 증권사 리포트 컨센서스 --------------------------------------------------

def test_analyst_report_collects_consensus():
    factory = factory_for(
        NVDA=FakeTicker(
            info=NVDA_INFO,
            recommendations=NVDA_RECOMMENDATIONS,
            upgrades_downgrades=NVDA_UPGRADES,
        )
    )
    report = collect_analyst_report("NVDA", factory, today=date(2026, 8, 19))

    assert report.target_price_mean == 210.5
    assert report.target_price_high == 275.0
    assert report.target_price_low == 120.0
    assert report.target_price_median == 215.0
    assert report.analyst_count == 62
    assert report.recommendation_mean == 1.34
    assert report.recommendation_key == "strong_buy"
    assert report.last_updated == date(2026, 8, 19)
    assert "yfinance" in report.source


def test_rating_distribution_uses_latest_period():
    factory = factory_for(
        NVDA=FakeTicker(info=NVDA_INFO, recommendations=NVDA_RECOMMENDATIONS)
    )
    dist = collect_analyst_report("NVDA", factory).rating_distribution

    assert dist is not None
    assert dist.period == "0m"
    assert dist.strong_buy == 40
    assert dist.buy == 18
    assert dist.hold == 4
    assert dist.sell == 0
    assert dist.strong_sell == 0


def test_upgrade_history_parsed_in_order():
    factory = factory_for(
        NVDA=FakeTicker(info=NVDA_INFO, upgrades_downgrades=NVDA_UPGRADES)
    )
    actions = collect_analyst_report("NVDA", factory).recent_actions

    assert len(actions) == 2
    assert actions[0].firm == "Morgan Stanley"
    assert actions[0].from_grade == "Equal-Weight"
    assert actions[0].to_grade == "Overweight"
    assert actions[0].action == "up"
    assert actions[0].action_date == date(2026, 8, 12)


def test_action_limit_respected():
    factory = factory_for(
        NVDA=FakeTicker(info=NVDA_INFO, upgrades_downgrades=NVDA_UPGRADES)
    )
    report = collect_analyst_report("NVDA", factory, action_limit=1)
    assert len(report.recent_actions) == 1


def test_optional_sections_degrade_without_killing_collection():
    """분포·이력이 없어도 컨센서스 본체는 살아야 한다."""
    factory = factory_for(NVDA=FakeTicker(info=NVDA_INFO))
    report = collect_analyst_report("NVDA", factory)

    assert report.target_price_mean == 210.5
    assert report.rating_distribution is None
    assert report.recent_actions == []


def test_analyst_report_missing_targets_are_none():
    factory = factory_for(X=FakeTicker(info={"recommendationKey": "hold"}))
    report = collect_analyst_report("X", factory)

    assert report.recommendation_key == "hold"
    assert report.target_price_mean is None
    assert report.analyst_count is None


def test_analyst_batch_isolates_failures():
    factory = factory_for(
        NVDA=FakeTicker(info=NVDA_INFO),
        BAD=FakeTicker(raise_on_info=TimeoutError("timeout")),
    )
    result = collect_analyst_reports_many(["NVDA", "BAD"], factory)

    assert [r.symbol for r in result.records] == ["NVDA"]
    assert "BAD" in result.errors


# --- watchlist -------------------------------------------------------------

def test_watchlist_loads_configured_symbols():
    items = load_watchlist()
    assert len(items) >= 1
    assert "NVDA" in load_symbols()
    assert all(item.symbol for item in items)


def test_watchlist_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_watchlist(tmp_path / "없는파일.yaml")


# --- pandas DataFrame 원천 형태 (실제 yfinance 반환 형태) ---------------------

def test_dataframe_source_is_supported():
    """실제 yfinance는 dict가 아닌 DataFrame을 반환한다."""
    pd = pytest.importorskip("pandas")

    factory = factory_for(
        NVDA=FakeTicker(
            info=NVDA_INFO,
            recommendations=pd.DataFrame(NVDA_RECOMMENDATIONS),
        )
    )
    dist = collect_analyst_report("NVDA", factory).rating_distribution

    assert dist is not None
    assert dist.period == "0m"
    assert dist.strong_buy == 40


def test_grade_date_from_dataframe_index_is_preserved():
    """회귀 방지: upgrades_downgrades는 공표일을 '인덱스'로 준다.

    to_dict(orient="records")는 인덱스를 버리므로, 되살리지 않으면
    모든 action_date 가 조용히 None 이 된다.
    """
    pd = pytest.importorskip("pandas")

    frame = pd.DataFrame(
        [{"Firm": "Morgan Stanley", "FromGrade": "Equal-Weight",
          "ToGrade": "Overweight", "Action": "up"}],
        index=pd.DatetimeIndex(["2026-08-12"], name="GradeDate"),
    )
    factory = factory_for(NVDA=FakeTicker(info=NVDA_INFO, upgrades_downgrades=frame))
    actions = collect_analyst_report("NVDA", factory).recent_actions

    assert len(actions) == 1
    assert actions[0].action_date == date(2026, 8, 12)
    assert actions[0].firm == "Morgan Stanley"


def test_empty_dataframe_yields_no_rows():
    pd = pytest.importorskip("pandas")
    factory = factory_for(
        NVDA=FakeTicker(info=NVDA_INFO, recommendations=pd.DataFrame(),
                        upgrades_downgrades=pd.DataFrame())
    )
    report = collect_analyst_report("NVDA", factory)

    assert report.rating_distribution is None
    assert report.recent_actions == []
