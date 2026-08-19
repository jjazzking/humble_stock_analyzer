from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class FundamentalData(BaseModel):
    """기업 펀더멘털 데이터 규격"""
    symbol: str
    market_cap: Optional[float] = Field(None, description="시가총액 (USD)")
    pe_ratio: Optional[float] = Field(None, description="트레일링 P/E (과거 PER)")
    forward_pe: Optional[float] = Field(None, description="포워드 P/E (선행 PER)")
    revenue_growth_yoy: Optional[float] = Field(None, description="전년 대비 매출 성장률 (%)")
    free_cash_flow: Optional[float] = Field(None, description="최근 잉여현금흐름 (FCF)")
    # 향후 원하는 펀더멘털 지표(ROE, 영업이익률 등)를 이곳에 손쉽게 추가 가능

class NarrativeData(BaseModel):
    """기업 투자 내러티브 및 핵심 이슈 규격"""
    symbol: str
    business_summary: Optional[str] = Field(None, description="주요 사업 및 AI 관련성 요약")
    key_catalysts: List[str] = Field(default_factory=list, description="주요 상승 모멘텀 / 촉매")
    risk_factors: List[str] = Field(default_factory=list, description="주요 리스크 요인")
    last_updated: Optional[date] = Field(None, description="최종 업데이트 일자")

class TechnicalData(BaseModel):
    """기술적 지표 및 눌림목 데이터 규격 (점수화 없는 순수 수학적 지표)"""
    symbol: str
    current_price: float = Field(..., description="현재 주가")
    sma_50: Optional[float] = Field(None, description="50일 단순이동평균")
    sma_200: Optional[float] = Field(None, description="200일 단순이동평균")
    distance_sma_50_pct: Optional[float] = Field(None, description="50일 이평선 대비 이격도 (%)")
    high_52w_drawdown_pct: Optional[float] = Field(None, description="52주 최고가 대비 하락률 (%)")
    rsi_14: Optional[float] = Field(None, description="14일 기준 RSI")
    # 향후 원하는 기술적 지표(볼린저 밴드, 거래량 등)를 이곳에 손쉽게 추가 가능

class AnalystRatingDistribution(BaseModel):
    """증권사 투자의견 분포 (특정 기준월의 의견별 애널리스트 수)"""
    period: Optional[str] = Field(None, description="집계 기준 구간 (예: 0m=당월, -1m=한달 전)")
    strong_buy: Optional[int] = Field(None, description="적극 매수 의견 수")
    buy: Optional[int] = Field(None, description="매수 의견 수")
    hold: Optional[int] = Field(None, description="중립 의견 수")
    sell: Optional[int] = Field(None, description="매도 의견 수")
    strong_sell: Optional[int] = Field(None, description="적극 매도 의견 수")


class AnalystAction(BaseModel):
    """증권사 투자의견 변경 이력 1건"""
    action_date: Optional[date] = Field(None, description="의견 변경 공표일")
    firm: Optional[str] = Field(None, description="증권사명")
    from_grade: Optional[str] = Field(None, description="변경 전 투자의견")
    to_grade: Optional[str] = Field(None, description="변경 후 투자의견")
    action: Optional[str] = Field(None, description="변경 유형 (up/down/init/main/reit 등 원문 그대로)")


class AnalystReportData(BaseModel):
    """증권사 리포트 컨센서스 규격

    주의: 여기 담기는 목표주가/투자의견은 외부 기관이 공표한 값을 가공 없이
    그대로 전달하는 것이다. 이 값들을 재료로 자체 점수/등급을 파생시키지 않는다.
    """
    symbol: str
    target_price_mean: Optional[float] = Field(None, description="목표주가 평균")
    target_price_high: Optional[float] = Field(None, description="목표주가 최고")
    target_price_low: Optional[float] = Field(None, description="목표주가 최저")
    target_price_median: Optional[float] = Field(None, description="목표주가 중앙값")
    analyst_count: Optional[int] = Field(None, description="커버리지 애널리스트 수")
    recommendation_mean: Optional[float] = Field(
        None, description="투자의견 평균 (출처 제공값. 1=적극매수 ~ 5=적극매도)"
    )
    recommendation_key: Optional[str] = Field(None, description="투자의견 요약 문자열 (출처 제공값)")
    rating_distribution: Optional[AnalystRatingDistribution] = Field(
        None, description="최신 기준월의 투자의견 분포"
    )
    recent_actions: List[AnalystAction] = Field(
        default_factory=list, description="최근 투자의견 변경 이력 (최신순)"
    )
    source: Optional[str] = Field(None, description="데이터 출처 표기")
    last_updated: Optional[date] = Field(None, description="수집 일자")
    # 향후 실적 추정치(EPS/매출 컨센서스) 등을 이곳에 손쉽게 추가 가능


class StockRecord(BaseModel):
    """개별 종목 종합 레코드"""
    symbol: str
    name: Optional[str] = None
    fundamentals: FundamentalData
    narrative: NarrativeData
    technicals: TechnicalData
    analyst_report: Optional[AnalystReportData] = Field(
        None, description="증권사 리포트 컨센서스 (미수집 시 None)"
    )
