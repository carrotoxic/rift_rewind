from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .player import Player
from .match import Match


class PlayerChapter(models.Model):
    """Represents a chapter/segment of a player's journey - used for the Journey page UI"""
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="chapters")
    
    # Chapter identification
    chapter_index = models.IntegerField(db_index=True)  # 1, 2, 3, etc. (chronological order)
    season = models.IntegerField(default=2025)  # Season year
    
    # Date range for this chapter
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    
    # Game indices (chronological match order for this player)
    start_game_idx = models.IntegerField()  # 1-based index of first match in chapter
    end_game_idx = models.IntegerField()  # 1-based index of last match in chapter
    
    # Agent-generated content
    title = models.CharField(max_length=200)  # Agent-generated chapter title (~140 chars)
    summary = models.TextField()  # Agent-generated narrative (2-3 sentences, ~240-360 chars)
    
    # Top champion for this chapter
    top_champion_id = models.IntegerField()
    top_champion_name = models.CharField(max_length=50)
    top_champion_icon_url = models.URLField(max_length=500, null=True, blank=True)
    top_champion_games = models.IntegerField(default=0)  # Number of games played with this champion
    
    # Aggregated stats (normalized 0-100 scores)
    games_count = models.IntegerField(default=0)
    win_rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )  # 0-1, will be converted to percentage in serializer
    kda_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )  # 0-100 normalized score
    cs_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )  # 0-100 normalized score
    damage_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )  # 0-100 normalized score
    vision_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )  # 0-100 normalized score
    
    # Raw aggregated metrics (for reference, not used in API). For AI Agent ingestion.
    raw_metrics = models.JSONField(default=dict, null=True, blank=True)
    
    # Matches in this chapter
    matches = models.ManyToManyField(Match, related_name="chapters", blank=True)
    
    class Meta:
        unique_together = [["player", "chapter_index", "season"]]
        ordering = ["chapter_index"]
        
    def __str__(self):
        return f"{self.player} - Chapter {self.chapter_index}: {self.title}"