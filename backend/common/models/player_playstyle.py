from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# PlayerPlaystyle (league_player_playstyle)
# =========================================================
@dataclass
class PlayerPlaystyle:
    id: Optional[int]
    player_id: Optional[int]                 # UNIQUE, nullable
    pro_player_id: Optional[int]             # UNIQUE, nullable

    aggressiveness: Optional[float] = None   # 0~100
    team_focus: Optional[float] = None       # 0~100
    objective_control: Optional[float] = None# 0~100
    vision_control: Optional[float] = None   # 0~100
    farm_efficiency: Optional[float] = None  # 0~100
    late_game_scaling: Optional[float] = None# 0~100

    playstyle_summary: Optional[str] = None
    raw_metrics: Optional[Dict[str, Any]] = None
    # 주의: DB에 "정확히 하나" 제약(CHECK)이 있으니, 생성 시 player_id 또는 pro_player_id 중 하나만 채워야 함.
