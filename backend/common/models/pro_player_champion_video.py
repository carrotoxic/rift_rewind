from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# ProPlayerChampionVideo (league_pro_player_champion_videos)
# =========================================================
@dataclass
class ProPlayerChampionVideo:
    id: Optional[int]
    player_id: int
    pro_player_id: int
    champion_id: int
    champion_name: str
    video_url: str
    video_title: Optional[str]
    match_id: Optional[str]
    key_points: str
    focus_areas: str
