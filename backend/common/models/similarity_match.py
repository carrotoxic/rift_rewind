from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .player import Player
from .pro_player import ProPlayer


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