from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        passsword = password
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=255, unique=True)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customusers',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customusers',
    )
