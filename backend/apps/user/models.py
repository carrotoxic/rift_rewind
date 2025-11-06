from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

"""
Login Page
"""

class Player(models.Model):
    """Represents a League of Legends player identified by Riot ID"""
    
    ROLE_CHOICES = [
        ("TOP", "Top"),
        ("JUNGLE", "Jungle"),
        ("MIDDLE", "Middle"),
        ("BOTTOM", "Bottom"),
        ("SUPPORT", "Support"),
    ]
    
    # Riot ID components
    game_name = models.CharField(max_length=100, db_index=True)
    tag_line = models.CharField(max_length=10, default="")
    puuid = models.CharField(max_length=200, unique=True, db_index=True)  # Riot's unique player identifier
    summoner_id = models.CharField(max_length=200, null=True, blank=True)
    
    # Region information
    region = models.CharField(max_length=10)  # e.g., 'NA1', 'KR', 'EUW1'
    
    # Player role (primary role based on most played)
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        null=True, 
        blank=True
    )  # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY

    # Favorite champion to tune the tone of the AI Agent.
    favorite_champion_id = models.IntegerField(null=True, blank=True)
    favorite_champion_name = models.CharField(max_length=50, null=True, blank=True)
    
    # Profile/summoner icon
    profile_icon_id = models.IntegerField(null=True, blank=True)  # For displaying summoner image
    
    class Meta:
        db_table = "league_players"
        unique_together = [["game_name", "tag_line", "region"]]
    
    def __str__(self):
        return f"{self.game_name}#{self.tag_line} ({self.region})"
    
    @property
    def riot_id(self):
        """Returns formatted Riot ID: gameName#tagLine"""
        return f"{self.game_name}#{self.tag_line}"


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


"""
Page1: “Your League Journey”
"""
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


"""
Page3: "Pro Player Similarity"
"""
#Question: shall we make abstract class for Player and ProPlayer?
class ProPlayer(models.Model):
    """Professional League of Legends players for similarity matching"""
    
    # Player information
    name = models.CharField(max_length=100, db_index=True)
    team = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=10)  # e.g., 'NA1', 'KR', 'EUW1'
    role = models.CharField(max_length=20)  # TOP, JUNGLE, MID, ADC, SUPPORT

    # Profile
    profile_icon_id = models.IntegerField(null=True, blank=True)  # For displaying pro player image
    
    # Riot identifiers (if available)
    puuid = models.CharField(max_length=200, null=True, blank=True, unique=True)
    game_name = models.CharField(max_length=100, null=True, blank=True)
    tag_line = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        db_table = "league_pro_players"
        indexes = [
            models.Index(fields=["region", "role"]),
        ]
    
    def __str__(self):
        team_str = f" ({self.team})" if self.team else ""
        return f"{self.name}{team_str} - {self.role}"


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


class SimilarityMatch(models.Model):
    """Similarity results between a player and pro players"""
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="similarity_matches")
    pro_player = models.ForeignKey(ProPlayer, on_delete=models.CASCADE, related_name="similarity_matches")
    
    # Similarity metrics
    similarity_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )  # Cosine similarity or other metric (0-1)
    
    # Agent-generated explanation of the similarity
    feature_explanation = models.TextField(null=True, blank=True)  # Agent-generated explanation

    class Meta:
        db_table = "league_similarity_matches"
        unique_together = [["player", "pro_player"]]
        indexes = [
            models.Index(fields=["player", "-similarity_score"]),
            models.Index(fields=["pro_player", "-similarity_score"]),
        ]
        ordering = ["-similarity_score"]
    
    def __str__(self):
        return f"{self.player} ↔ {self.pro_player} (Score: {self.similarity_score:.3f})"


"""
Page4: "Champion Pool Suggestions"
"""
class ChampionRecommendation(models.Model):
    """Champion recommendations for players"""
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="champion_recommendations")
    
    # Champion information
    champion_id = models.IntegerField()
    champion_name = models.CharField(max_length=50)
    champion_icon_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Agent-generated explanation
    reason = models.TextField()  # Why this champion is recommended
    
    # Ranking (1 = top recommendation, 2 = second, 3 = third)
    rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    
    class Meta:
        db_table = "league_champion_recommendations"
        unique_together = [["player", "rank"]]
        ordering = ["rank"]
    
    def __str__(self):
        return f"{self.player} - {self.champion_name} (Rank {self.rank})"


"""
Page5: "Pro Player Game Video with Suggested Champion"
"""
class ProPlayerChampionVideo(models.Model):
    """Pro player video recommendations for chosen champions"""
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="champion_videos")
    pro_player = models.ForeignKey(ProPlayer, on_delete=models.CASCADE, related_name="champion_videos")
    
    # Champion information
    champion_id = models.IntegerField()
    champion_name = models.CharField(max_length=50)
    
    # Video information
    video_url = models.URLField(max_length=500)  # Video link (YouTube, Twitch, etc.)
    video_title = models.CharField(max_length=200, null=True, blank=True)
    match_id = models.CharField(max_length=100, null=True, blank=True)  # If available from Riot API
    
    # AI agent-generated content
    key_points = models.TextField()  # Explanation of key points in the video
    focus_areas = models.TextField()  # Which parts player should focus on watching
    
    class Meta:
        db_table = "league_pro_player_champion_videos"
        indexes = [
            models.Index(fields=["player", "champion_id"]),
            models.Index(fields=["pro_player", "champion_id"]),
        ]
    
    def __str__(self):
        return f"{self.pro_player} - {self.champion_name} (for {self.player})"
