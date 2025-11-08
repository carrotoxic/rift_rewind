from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# =========================================================
# SimilarityMatch (league_similarity_matches)
# =========================================================
@dataclass
class SimilarityMatch:
    id: Optional[int]
    player_id: int
    pro_player_id: int
    similarity_score: float                  # 0~1
    feature_explanation: Optional[str] = None

