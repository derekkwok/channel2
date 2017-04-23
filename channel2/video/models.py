import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone

from channel2.account.models import User

# Number of hours the link is valid for.
LINK_VALID_DURATION = 4


class VideoLink(models.Model):

    user = models.ForeignKey(User)
    link_path = models.CharField(max_length=128, unique=True)
    file_path = models.CharField(max_length=1024)
    created_on = models.DateTimeField(auto_now=True)
    expires_on = models.DateTimeField(db_index=True)

    class Meta:
        db_table = 'video_link'
        index_together = [('user', 'file_path')]

    @staticmethod
    def create(user, file_path):
        link_path = secrets.token_urlsafe(128)
        expires_on = timezone.now() + timedelta(hours=LINK_VALID_DURATION)
        return VideoLink.objects.create(
            user=user, file_path=file_path, link_path=link_path,
            expires_on=expires_on)
