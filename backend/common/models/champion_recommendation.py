from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# ChampionRecommendation (league_champion_recommendations)
# =========================================================
@dataclass
class ChampionRecommendation:
    id: Optional[int]
    player_id: int
    champion_id: int
    champion_name: str
    champion_icon_url: Optional[str]
    reason: str
    rank: int                                # 1~3 (unique per player_id)
