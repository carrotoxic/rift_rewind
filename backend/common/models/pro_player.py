from django.db import models


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

