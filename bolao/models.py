from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone

class BettingPool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def generate_access_token(self, max_uses=None, expires_at=None):
        token = get_random_string(length=32)
        AccessToken.objects.create(
            pool=self,
            token=token,
            max_uses=max_uses,
            expires_at=expires_at
        )
        return token

class AccessToken(models.Model):
    pool = models.ForeignKey(BettingPool, on_delete=models.CASCADE, related_name='access_tokens')
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_uses = models.IntegerField(null=True, blank=True)
    uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Token for {self.pool.name}"

    def is_valid(self):
        if not self.is_active:
            return False
        
        if self.expires_at and self.expires_at < timezone.now():
            return False
            
        if self.max_uses and self.uses >= self.max_uses:
            return False
            
        return True

    def use(self):
        if not self.is_valid():
            return False
            
        self.uses += 1
        if self.max_uses and self.uses >= self.max_uses:
            self.is_active = False
        self.save()
        return True