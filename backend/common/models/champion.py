from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


# =========================================================
# Champion (league_champions)
# =========================================================
@dataclass
class Champion:
    id: Optional[int]                     # BIGSERIAL PK (DB 생성)
    champion_id: int                      # UNIQUE
    champion_key: str                     # UNIQUE
    name: str
    title: str = ""
    image_url: str = ""
