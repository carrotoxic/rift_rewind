from django.db import models

# Assuming the Champion model is already defined elsewhere
# from .models import Champion

class RiotUser(models.Model):
    """
    Basic Riot Games user (Summoner) information.
    - No authentication/login system
    - riot_id (e.g., "Faker#KR1") is used as the primary key
    """
    ROLE_CHOICES = [
        ("TOP", "Top"),
        ("JUNGLE", "Jungle"),
        ("MIDDLE", "Middle"),
        ("BOTTOM", "Bottom"),
        ("SUPPORT", "Support"),
    ]

    # Example: "gameName#tagLine"
    riot_id = models.CharField(max_length=120, primary_key=True)

    # Example: "KR", "NA1", "EUW1"
    region = models.CharField(max_length=10, db_index=True)

    # Player’s primary role (lane position)
    main_role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Player’s favorite champion (nullable)
    favorite_champion = models.ForeignKey(
        "Champion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favorited_by_users",
    )

    # Last time the player was seen or synced from Riot API
    last_seen_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "league_riot_users"
        indexes = [
            models.Index(fields=["region", "main_role"]),
        ]

    def __str__(self):
        return self.riot_id
