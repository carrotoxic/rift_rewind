from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


# =========================================================
# RiotUser (league_riot_users)
# =========================================================
@dataclass
class RiotUser:
    riot_id: str                          # PK, e.g. "gameName#tagLine"
    region: str
    main_role: str                        # 'TOP','JUNGLE','MIDDLE','BOTTOM','SUPPORT'
    favorite_champion_id: Optional[int] = None   # FK -> league_champions.id
    last_seen_at: Optional[datetime] = None      # timestamptz
