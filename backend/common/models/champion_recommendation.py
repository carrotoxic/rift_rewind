from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .player import Player


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