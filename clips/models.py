from django.db import models
from django.conf import settings


class Clip(models.Model):
    """
    Basic clip model for the video feed.
    Many to one relation to the user.
    """
    objects = models.Manager()
    url = models.URLField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name="clips",
    )


class ClipVote(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clip_votes",
    )
    clip = models.ForeignKey(
        Clip,
        null=True,
        on_delete=models.CASCADE,
        related_name="clip_votes"
    )
