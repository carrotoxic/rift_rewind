from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# PlayerMatchMetrics (league_player_match_metrics)
# =========================================================
@dataclass
class PlayerMatchMetrics:
    id: Optional[int]
    match_id: int                          # UNIQUE, FK -> league_matches.id
    player_id: int                         # FK -> league_players.id

    champion_id: int
    champion_name: str
    role: Optional[str] = None             # enum set
    lane: Optional[str] = None

    cs_per_min: Optional[float] = None
    gold_per_min: Optional[float] = None
    damage_per_min: Optional[float] = None
    damage_share: Optional[float] = None   # 0~1
    kill_participation: Optional[float] = None  # 0~1

    kills: int = 0
    deaths: int = 0
    assists: int = 0
    kda_ratio: Optional[float] = None

    win: bool = False
    team_id: Optional[int] = None          # 100 or 200
    participant_id: Optional[int] = None   # smallint
    game_duration: Optional[int] = None    # seconds

    vision_score: Optional[int] = None
    vision_score_per_min: Optional[float] = None
    gold_earned: Optional[int] = None
    total_damage_dealt: Optional[int] = None
    total_damage_taken: Optional[int] = None
    total_heal: Optional[int] = None
    total_minions_killed: Optional[int] = None
    neutral_minions_killed: Optional[int] = None
    wards_placed: Optional[int] = None
    wards_killed: Optional[int] = None
    first_blood: bool = False
    first_blood_assist: bool = False
    first_tower: bool = False
    first_tower_assist: bool = False

    items: Optional[List[int]] = None                  # len<=7
    summoner_spells: Optional[List[str]] = None        # len<=2
    rune_setup: Optional[Dict[str, Any]] = None
    skill_order: Optional[List[str]] = None            # len<=18
    damage_breakdown: Optional[Dict[str, Any]] = None
    objective_contribution: Optional[Dict[str, Any]] = None
    analysis_json: Optional[Dict[str, Any]] = None

    match_recorded_at: int = 0             # = match_timestamp; for indexing

