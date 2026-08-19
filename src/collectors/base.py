"""수집기 공통 기반 모듈.

설계 원칙 (CLAUDE.md 연계):
- 값이 없으면 추정하지 않고 None으로 남긴다.
- "수집 실패"와 "원래 값이 없음"을 구분한다. 전자는 CollectorError로 보고하고,
  후자만 None이 된다. 둘을 뭉뚱그리면 장애가 N/A로 위장되어 표시된다.
- 지표 추가는 각 수집기의 FIELD_SPECS 에 FieldSpec 한 줄을 더하는 것으로 끝난다.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field as dataclass_field
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Protocol


class CollectorError(RuntimeError):
    """원천 데이터 조회 자체가 실패했을 때 발생. 값 부재(None)와 구분된다."""

    def __init__(self, symbol: str, message: str) -> None:
        super().__init__(f"[{symbol}] {message}")
        self.symbol = symbol
        self.message = message


class TickerLike(Protocol):
    """yfinance.Ticker 중 본 프로젝트가 사용하는 최소 인터페이스.

    테스트에서 네트워크 없이 가짜 객체를 주입할 수 있도록 프로토콜로 분리한다.
    """

    @property
    def info(self) -> Mapping[str, Any]: ...


TickerFactory = Callable[[str], TickerLike]


def default_ticker_factory(symbol: str) -> TickerLike:
    """기본 원천: yfinance. import를 함수 안에 두어 테스트 시 불필요한 로딩을 피한다."""
    import yfinance as yf

    return yf.Ticker(symbol)


def is_missing(value: Any) -> bool:
    """원천 데이터에서 '값 없음'으로 취급할 대상인지 판정.

    yfinance는 결측을 None, NaN, 빈 문자열, 무한대 등 제각각으로 돌려주므로
    한 곳에서 일괄 판정한다.
    """
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return True
    # pandas.NA / NaT 등 자기 자신과 같지 않은 결측 표현
    try:
        if value != value:  # noqa: PLR0124
            return True
    except (TypeError, ValueError):
        pass
    return False


@dataclass(frozen=True)
class FieldSpec:
    """원천 데이터의 키 하나를 스키마 필드 하나에 대응시키는 규칙.

    새 지표를 추가하려면 이 규칙 한 줄만 FIELD_SPECS에 더하면 된다.
    """

    field: str                                   # 대상 스키마 필드명
    source_key: str                              # 원천 데이터(dict)의 키
    transform: Optional[Callable[[Any], Any]] = None  # 단위 변환 등 순수 변환 함수
    note: str = ""                               # 변환 근거 메모


def to_percent(value: Any) -> Optional[float]:
    """비율(0.12)을 퍼센트(12.0)로 변환. 원천이 소수 비율로 주는 항목에 사용."""
    return round(float(value) * 100, 4)


def apply_specs(source: Mapping[str, Any], specs: Iterable[FieldSpec]) -> Dict[str, Any]:
    """원천 dict에 FieldSpec 목록을 적용해 스키마 필드 dict를 만든다.

    값이 없거나 변환에 실패하면 임의 보정 없이 None을 넣는다.
    """
    result: Dict[str, Any] = {}
    for spec in specs:
        raw = source.get(spec.source_key)
        if is_missing(raw):
            result[spec.field] = None
            continue
        if spec.transform is None:
            result[spec.field] = raw
            continue
        try:
            result[spec.field] = spec.transform(raw)
        except (TypeError, ValueError):
            # 변환 불가 값을 추측해 채우지 않는다.
            result[spec.field] = None
    return result


@dataclass
class BatchResult:
    """여러 종목 수집 결과. 일부 종목 실패가 배치 전체를 중단시키지 않도록 분리 보관."""

    records: List[Any] = dataclass_field(default_factory=list)
    errors: Dict[str, str] = dataclass_field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors


def collect_many(
    symbols: Iterable[str],
    collect_one: Callable[[str], Any],
) -> BatchResult:
    """종목별 수집 함수를 순회 적용하고 성공/실패를 분리해 반환."""
    result = BatchResult()
    for symbol in symbols:
        try:
            result.records.append(collect_one(symbol))
        except CollectorError as exc:
            result.errors[symbol] = exc.message
        except Exception as exc:  # 예상 못 한 원천 라이브러리 오류도 배치를 죽이지 않는다
            result.errors[symbol] = f"{type(exc).__name__}: {exc}"
    return result


def fetch_info(symbol: str, ticker_factory: TickerFactory) -> Mapping[str, Any]:
    """Ticker.info 조회. 조회 실패는 CollectorError로 승격시킨다."""
    try:
        info = ticker_factory(symbol).info
    except Exception as exc:
        raise CollectorError(symbol, f"원천 조회 실패: {type(exc).__name__}: {exc}") from exc
    if not info:
        raise CollectorError(symbol, "원천이 빈 응답을 반환했습니다 (심볼 오류 가능성)")
    return info
