from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# ProPlayer (league_pro_players)
# =========================================================
@dataclass
class ProPlayer:
    id: Optional[int]
    name: str
    team: Optional[str]
    region: str
    role: str                              # enum set
    profile_icon_id: Optional[int] = None
    puuid: Optional[str] = None            # UNIQUE, nullable
    game_name: Optional[str] = None
    tag_line: Optional[str] = None

