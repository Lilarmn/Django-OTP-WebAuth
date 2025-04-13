from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email....")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)  # رمز هش می‌شود
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # اختیاری (بدون رمز عبور)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # WebAuthn fields:
    credential_id = models.BinaryField(null=True, blank=True)
    credential_public_key = models.BinaryField(null=True, blank=True)
    sign_count = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()



class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return timezone.now() < self.expires_at and not self.is_used


class WebAuthnKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    credential_id = models.CharField(max_length=255, unique=True)
    public_key = models.TextField()
    sign_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)
