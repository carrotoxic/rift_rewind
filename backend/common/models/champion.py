from django.db import models


class Champion(models.Model):
    """Basic static champion information (LoL)"""

    champion_id = models.IntegerField(unique=True, db_index=True)
    champion_key = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = "league_champions"
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name