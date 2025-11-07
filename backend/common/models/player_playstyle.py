from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .player import Player
from .pro_player import ProPlayer


class PlayerPlaystyle(models.Model):
    """Normalized playstyle metrics for players and pro players - used for similarity matching"""
    
    # Link to player (can be regular Player or ProPlayer)
    player = models.OneToOneField(
        Player, on_delete=models.CASCADE, related_name="playstyle", null=True, blank=True
    )
    pro_player = models.OneToOneField(
        ProPlayer, on_delete=models.CASCADE, related_name="playstyle", null=True, blank=True
    )
    
    # Playstyle metrics (normalized 0-100 scores)
    aggressiveness = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, blank=True
    )  # Early game aggression, solo kills, tower dives
    team_focus = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, blank=True
    )  # Kill participation, team fight presence
    objective_control = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, blank=True
    )  # Dragon/baron participation rate
    vision_control = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, blank=True
    )  # Ward placement patterns, vision score
    farm_efficiency = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, blank=True
    )  # CS/min relative to role average
    late_game_scaling = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, blank=True
    )  # Performance improvement in long games
    
    # Additional playstyle data
    playstyle_summary = models.TextField(null=True, blank=True)  # Agent-generated playstyle description
    raw_metrics = models.JSONField(default=dict, null=True, blank=True)  # Raw calculation data for AI Agent ingestion
    
    class Meta:
        db_table = "league_player_playstyle"
    
    def __str__(self):
        if self.player:
            return f"Playstyle for {self.player}"
        elif self.pro_player:
            return f"Playstyle for Pro {self.pro_player}"
        return "Playstyle"