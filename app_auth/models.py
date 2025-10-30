import hashlib
from django.db import models
from django.conf import settings
from django.utils import timezone

class TokenBlacklist(models.Model):
    """
    Модель для черного списка JWT токенов
    """
    token_hash = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'auth_token_blacklist'
        verbose_name = 'Токен в черном списке'
        verbose_name_plural = 'Токены в черном списке'
        indexes = [
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"Blacklisted token for {self.user.email}"
    
    @classmethod
    def add_token(cls, token, user, reason=''):
        """
        Добавляет токен в черный список
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        try:
            import jwt
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            expires_at = timezone.datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        except Exception:
            expires_at = timezone.now() + timezone.timedelta(hours=24)
        return cls.objects.create(
            token_hash=token_hash,
            user=user,
            expires_at=expires_at,
            reason=reason
        )
    
    @classmethod
    def is_token_blacklisted(cls, token):
        """
        Проверяет, находится ли токен в черном списке
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return cls.objects.filter(
            token_hash=token_hash,
            expires_at__gt=timezone.now()
        ).exists()