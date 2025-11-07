from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from .player import Player
from .match import Match


class PlayerMatchMetrics(models.Model):
    """Processed player metrics per match - structured data for analysis"""
    
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name="metrics")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_metrics")
    
    # Champion and role
    champion_id = models.IntegerField()
    champion_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, null=True, blank=True)  # TOP, JUNGLE, MID, ADC, SUPPORT
    lane = models.CharField(max_length=20, null=True, blank=True)  # TOP, JUNGLE, MIDDLE, BOTTOM
    
    # Core metrics
    cs_per_min = models.FloatField(null=True, blank=True)  # Creep score per minute
    gold_per_min = models.FloatField(null=True, blank=True)
    damage_per_min = models.FloatField(null=True, blank=True)
    damage_share = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )  # Percentage of team damage (0.0-1.0)
    kill_participation = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )  # Portion of team kills contributed to (0.0-1.0)
    
    # KDA
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    kda_ratio = models.FloatField(null=True, blank=True)  # (Kills + Assists) / Deaths
    
    # Game outcome
    win = models.BooleanField(default=False)
    team_id = models.IntegerField(null=True, blank=True)  # 100 (blue) or 200 (red)
    participant_id = models.PositiveSmallIntegerField(null=True, blank=True)
    game_duration = models.PositiveIntegerField(null=True, blank=True)  # Seconds
    
    # Additional metrics
    vision_score = models.IntegerField(null=True, blank=True)
    vision_score_per_min = models.FloatField(null=True, blank=True)
    gold_earned = models.IntegerField(null=True, blank=True)
    total_damage_dealt = models.IntegerField(null=True, blank=True)
    total_damage_taken = models.IntegerField(null=True, blank=True)
    total_heal = models.IntegerField(null=True, blank=True)
    total_minions_killed = models.IntegerField(null=True, blank=True)
    neutral_minions_killed = models.IntegerField(null=True, blank=True)
    wards_placed = models.IntegerField(null=True, blank=True)
    wards_killed = models.IntegerField(null=True, blank=True)
    first_blood = models.BooleanField(default=False)
    first_blood_assist = models.BooleanField(default=False)
    first_tower = models.BooleanField(default=False)
    first_tower_assist = models.BooleanField(default=False)
    items = ArrayField(
        base_field=models.PositiveIntegerField(),
        size=7,
        null=True,
        blank=True,
        default=list
    )  # 6 inventory slots + trinket
    summoner_spells = ArrayField(
        base_field=models.CharField(max_length=30),
        size=2,
        null=True,
        blank=True,
        default=list
    )
    rune_setup = models.JSONField(default=dict, null=True, blank=True)  # Primary + secondary runes
    skill_order = ArrayField(
        base_field=models.CharField(max_length=5),
        size=18,
        null=True,
        blank=True,
        default=list
    )  # Ability level-up order
    damage_breakdown = models.JSONField(default=dict, null=True, blank=True)
    objective_contribution = models.JSONField(default=dict, null=True, blank=True)
    
    # LLM-friendly JSON for analysis (structured summary)
    analysis_json = models.JSONField(default=dict, null=True, blank=True)
    
    # Match timestamp for time-series analysis
    match_timestamp = models.BigIntegerField(db_index=True)
    
    class Meta:
        db_table = "league_player_match_metrics"
        indexes = [
            models.Index(fields=["player", "-match_timestamp"]),
            models.Index(fields=["champion_id"]),
            models.Index(fields=["role"]),
            models.Index(fields=["win"]),
        ]
        ordering = ["-match_timestamp"]
    
    def __str__(self):
        return f"{self.player} - {self.champion_name} ({self.match.match_id})"