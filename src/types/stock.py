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

class StockRecord(BaseModel):
    """개별 종목 종합 레코드"""
    symbol: str
    name: Optional[str] = None
    fundamentals: FundamentalData
    narrative: NarrativeData
    technicals: TechnicalData
