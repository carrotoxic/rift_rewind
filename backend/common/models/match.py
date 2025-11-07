from django.db import models
from .player import Player


class Match(models.Model):
    """Raw match data from League API, stored before processing"""
    
    match_id = models.CharField(max_length=100, unique=True, db_index=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="matches")
    raw_data = models.JSONField(default=dict)  # Full match data from API
    match_timestamp = models.BigIntegerField(db_index=True)  # For ordering/querying
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        db_table = "league_matches"
        ordering = ["-match_timestamp"]
    
    def __str__(self):
        return f"Match {self.match_id} - {self.player}"
