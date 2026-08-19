"""config/watchlist.yaml 로더."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field

DEFAULT_WATCHLIST_PATH = Path(__file__).resolve().parents[2] / "config" / "watchlist.yaml"


class WatchlistItem(BaseModel):
    """감시 종목 1건"""
    symbol: str
    name: Optional[str] = Field(None, description="표시용 종목명")
    category: Optional[str] = Field(None, description="분류 (AI 반도체, 클라우드 등)")


def load_watchlist(path: Optional[Path] = None) -> List[WatchlistItem]:
    """감시 종목 목록을 읽어 검증된 모델 목록으로 반환."""
    target = Path(path) if path else DEFAULT_WATCHLIST_PATH
    if not target.exists():
        raise FileNotFoundError(f"watchlist 파일을 찾을 수 없습니다: {target}")

    raw = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    tickers = raw.get("tickers") or []
    return [WatchlistItem(**item) for item in tickers]


def load_symbols(path: Optional[Path] = None) -> List[str]:
    """감시 종목의 심볼만 반환."""
    return [item.symbol for item in load_watchlist(path)]
