from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from .player import Player
from .match import Match


class PlayerMatchMetrics(models.Model):
    """Processed player metrics per match - structured data for analysis"""
    
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name="metrics")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_metrics")
    
    # -------- Match metadata (denormalized for fast filtering/partitioning) --------
    patch = models.CharField(max_length=16, null=True, blank=True, db_index=True)      # e.g., "14.21"
    queue_id = models.IntegerField(null=True, blank=True, db_index=True)               # 400/420/430/440
    match_timestamp = models.BigIntegerField(db_index=True)                            # unix ms/sec (as ingested)

    # -------- Champion and role --------
    champion_id = models.IntegerField()
    champion_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, null=True, blank=True)   # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    lane = models.CharField(max_length=20, null=True, blank=True)   # TOP, JUNGLE, MIDDLE, BOTTOM

    # -------- Core per-minute shares/rates (primary LLM surface) --------
    cs_per_min = models.FloatField(null=True, blank=True)
    gold_per_min = models.FloatField(null=True, blank=True)
    damage_per_min = models.FloatField(null=True, blank=True)
    damage_share = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )  # % of team damage
    kill_participation = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )  # % of team kills

    # -------- KDA & outcome --------
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    kda_ratio = models.FloatField(null=True, blank=True)  # (K+A)/D
    win = models.BooleanField(default=False)
    team_id = models.IntegerField(null=True, blank=True)  # 100 or 200
    participant_id = models.PositiveSmallIntegerField(null=True, blank=True)
    game_duration = models.PositiveIntegerField(null=True, blank=True)  # seconds

    # -------- Vision & map awareness --------
    vision_score = models.IntegerField(null=True, blank=True)
    vision_score_per_min = models.FloatField(null=True, blank=True)
    vision_score_adv = models.FloatField(null=True, blank=True)  # advantage vs lane opponent
    wards_placed = models.IntegerField(null=True, blank=True)
    wards_killed = models.IntegerField(null=True, blank=True)
    wards_per_min = models.FloatField(null=True, blank=True)
    ctrl_wards_bought = models.IntegerField(null=True, blank=True)
    ctrl_wards_per_game = models.FloatField(null=True, blank=True)
    ctrl_ward_coverage = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    early_ward_takedowns = models.FloatField(null=True, blank=True)
    two_wards_sweeper_flag = models.BooleanField(default=False)

    # -------- Raw totals for context --------
    gold_earned = models.IntegerField(null=True, blank=True)
    total_damage_dealt = models.IntegerField(null=True, blank=True)
    total_damage_taken = models.IntegerField(null=True, blank=True)
    total_heal = models.IntegerField(null=True, blank=True)
    total_minions_killed = models.IntegerField(null=True, blank=True)
    neutral_minions_killed = models.IntegerField(null=True, blank=True)

    # -------- Firsts / early events --------
    first_blood = models.BooleanField(default=False)
    first_blood_assist = models.BooleanField(default=False)
    first_tower = models.BooleanField(default=False)
    first_tower_assist = models.BooleanField(default=False)

    # -------- Aggression & lane pressure --------
    solo_kill_flag = models.BooleanField(default=False)
    quick_solo_kills_flag = models.BooleanField(default=False)
    outnumbered_kill_flag = models.BooleanField(default=False)
    first_blood_participation_flag = models.BooleanField(default=False)
    kills_near_enemy_turret_flag = models.BooleanField(default=False)
    early_tower_damage_flag = models.BooleanField(default=False)
    max_cs_advantage = models.FloatField(null=True, blank=True)
    max_level_lead = models.FloatField(null=True, blank=True)
    laning_phase_advantage_flag = models.BooleanField(default=False)
    kills_under_own_turret_flag = models.BooleanField(default=False)
    dive_participation_flag = models.BooleanField(default=False)

    # -------- Teamplay & utility --------
    full_team_takedown_flag = models.BooleanField(default=False)
    immobilize_and_kill = models.FloatField(null=True, blank=True)
    pick_kill_with_ally = models.FloatField(null=True, blank=True)
    save_ally_from_death_flag = models.BooleanField(default=False)
    cc_time_s = models.FloatField(null=True, blank=True)
    heal_shield_on_mates = models.FloatField(null=True, blank=True)

    # -------- Objectives --------
    dragon_takedowns = models.FloatField(null=True, blank=True)
    baron_takedowns = models.FloatField(null=True, blank=True)
    rift_herald_takedowns = models.FloatField(null=True, blank=True)
    epic_monster_steals = models.FloatField(null=True, blank=True)
    obj_timing_hits = models.FloatField(null=True, blank=True)  # kills near spawn windows
    epic_monster_damage_share = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.0)]
    )
    earliest_dragon_time_s = models.FloatField(null=True, blank=True)
    objective_contribution = models.JSONField(default=dict, null=True, blank=True)

    # -------- Farming & economy --------
    cs_at_10 = models.FloatField(null=True, blank=True)
    jungle_cs_at_10 = models.FloatField(null=True, blank=True)
    item_purchase_rate_pm = models.FloatField(null=True, blank=True)
    gold_efficiency_raw = models.FloatField(null=True, blank=True)  # gold / total damage (proxy)

    # -------- Scaling & game context --------
    is_long_game = models.BooleanField(default=False)
    is_short_game = models.BooleanField(default=False)
    scaling_champion_flag = models.BooleanField(default=False)  # set via champ metadata if desired

    # -------- Damage profile & survivability --------
    damage_to_champs_ratio = models.FloatField(null=True, blank=True)
    damage_per_gold = models.FloatField(null=True, blank=True)
    kda_to_damage_ratio = models.FloatField(null=True, blank=True)
    damage_taken_share = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    damage_mitigated_rate = models.FloatField(null=True, blank=True)  # self-mitigated / taken
    survivability_score = models.FloatField(null=True, blank=True)

    # -------- Consistency markers --------
    kda_raw = models.FloatField(null=True, blank=True)
    high_impact_game_flag = models.BooleanField(default=False)
    low_impact_game_flag = models.BooleanField(default=False)
    behind_early_win_flag = models.BooleanField(default=False)

    # -------- Role-specific & split push / jungle --------
    champion_diversity_token = models.CharField(max_length=32, null=True, blank=True)
    preferred_champion_token = models.CharField(max_length=32, null=True, blank=True)
    jungle_clear_efficiency_pm = models.FloatField(null=True, blank=True)
    peel_score_raw = models.FloatField(null=True, blank=True)
    split_push_score_raw = models.FloatField(null=True, blank=True)

    # -------- Gear / runes / spells --------
    items = ArrayField(
        base_field=models.PositiveIntegerField(),
        size=7,
        null=True,
        blank=True,
        default=list,
        help_text="6 inventory slots + trinket",
    )
    summoner_spells = ArrayField(
        base_field=models.CharField(max_length=30),
        size=2,
        null=True,
        blank=True,
        default=list,
    )
    rune_setup = models.JSONField(default=dict, null=True, blank=True)
    damage_breakdown = models.JSONField(default=dict, null=True, blank=True)

    # -------- LLM-friendly payloads --------
    tags = ArrayField(base_field=models.CharField(max_length=32), null=True, blank=True, default=list)
    analysis_json = models.JSONField(default=dict, null=True, blank=True)
    analysis_summary = models.TextField(null=True, blank=True)  # 1–2 sentence cached blurb

    class Meta:
        db_table = "league_player_match_metrics"
        indexes = [
            models.Index(fields=["player", "-match_timestamp"]),
            models.Index(fields=["champion_id"]),
            models.Index(fields=["role"]),
            models.Index(fields=["win"]),
            models.Index(fields=["patch", "role"]),
            models.Index(fields=["queue_id"]),
        ]
        ordering = ["-match_timestamp"]
    
    def __str__(self):
        return f"{self.player} - {self.champion_name} ({self.match.match_id})"