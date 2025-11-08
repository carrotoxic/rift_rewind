from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


# =========================================================
# Match (league_matches)
# =========================================================
@dataclass
class Match:
    id: Optional[int]
    match_id: str                          # UNIQUE
    player_id: int                         # FK -> league_players.id
    raw_data: Dict[str, Any]               # jsonb
    match_timestamp: int                   # epoch(ms) or (s) – DB 그대로
    is_processed: bool = False

