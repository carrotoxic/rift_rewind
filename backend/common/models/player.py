from django.db import models


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