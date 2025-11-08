from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# PlayerChapter (league_player_chapters)
# =========================================================
@dataclass
class PlayerChapter:
    id: Optional[int]
    player_id: int
    chapter_index: int
    season: int = 2025

    start_date: datetime = field(default_factory=datetime.utcnow)  # date-only in DB
    end_date: datetime = field(default_factory=datetime.utcnow)    # date-only in DB

    start_game_idx: int = 1
    end_game_idx: int = 1

    title: str = ""
    summary: str = ""

    top_champion_id: int = 0
    top_champion_name: str = ""
    top_champion_icon_url: Optional[str] = None
    top_champion_games: int = 0

    games_count: int = 0
    win_rate: float = 0.0                   # 0~1
    kda_score: float = 0.0                  # 0~100
    cs_score: float = 0.0                   # 0~100
    damage_score: float = 0.0               # 0~100
    vision_score: float = 0.0               # 0~100

    raw_metrics: Optional[Dict[str, Any]] = None

