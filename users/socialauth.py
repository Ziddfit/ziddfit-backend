import uuid
from django.db import models
from django.conf import settings


class SocialAuth(models.Model):

    PROVIDER_CHOICES = [
        ('GOOGLE', 'Google'),
        ('APPLE', 'Apple'),
        ('FACEBOOK', 'Facebook'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='social_auths' 
    )                              
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    provider_uid = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'provider']]
        indexes = [
            models.Index(fields=['provider', 'provider_uid'])
        ]

    def __str__(self):
        return f"{self.user.email} - {self.provider}"