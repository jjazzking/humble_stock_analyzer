from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date

class FundamentalData(BaseModel):
    symbol: str
    market_cap: Optional[float] = Field(None, description="Market Cap in USD")
    pe_ratio: Optional[float] = Field(None, description="Trailing P/E")
    forward_pe: Optional[float] = Field(None, description="Forward P/E")
    revenue_growth_yoy: Optional[float] = Field(None, description="YoY Revenue Growth %")
    free_cash_flow: Optional[float] = Field(None, description="Latest FCF")
    # Future metrics can be added here without breaking existing code

class NarrativeData(BaseModel):
    symbol: str
    key_catalysts: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    last_updated: Optional[date] = None

class TechnicalData(BaseModel):
    symbol: str
    current_price: float
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    distance_sma_50_pct: Optional[float] = Field(None, description="Distance from 50 SMA (%)")
    high_52w_drawdown_pct: Optional[float] = Field(None, description="Drawdown from 52w High (%)")
    rsi_14: Optional[float] = None
    # Future technical metrics can be added here

class StockRecord(BaseModel):
    symbol: str
    fundamentals: FundamentalData
    narrative: NarrativeData
    technicals: TechnicalData
