from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# Player (league_players)
# =========================================================
@dataclass
class Player:
    id: Optional[int]                     # BIGSERIAL PK
    game_name: str
    tag_line: str = ""
    puuid: str = ""                       # UNIQUE
    summoner_id: Optional[str] = None
    region: str = ""
    role: Optional[str] = None            # nullable; same enum set as above
    favorite_champion_id: Optional[int] = None
    favorite_champion_name: Optional[str] = None
    profile_icon_id: Optional[int] = None

