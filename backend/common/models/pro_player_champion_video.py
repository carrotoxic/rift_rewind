from django.db import models
from .player import Player
from .pro_player import ProPlayer


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
