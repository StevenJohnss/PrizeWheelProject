"""
Database models.
"""
import uuid
import os
from django.db.models.functions import Now
from django.db.models import Q    

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def upload_image_file_path(instance, filename):
    """Generate file path for new prize image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# class Recipe(models.Model):
#     """Recipe object."""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     time_minutes = models.IntegerField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     link = models.CharField(max_length=255, blank=True)
#     tags = models.ManyToManyField('Tag')
#     ingredients = models.ManyToManyField('Ingredient')
#     image = models.ImageField(null=True, upload_to=recipe_image_file_path)

#     def __str__(self):
#         return self.title


class Spin(models.Model):
    """user Spins"""
    remaining_spins = models.IntegerField(default=3)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                       verbose_name=("user_spins"),
                                       on_delete=models.CASCADE,
                                       primary_key=True)

    def __str__(self):
        return f"{self.remaining_spins}"


class Prize(models.Model):
    """Prizes."""
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    remaining_quantity = models.IntegerField(default=10)
    image= models.ImageField(null=True, blank=True, upload_to=upload_image_file_path, height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.name

class UserPrize(models.Model):
    """User Prize."""
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE,)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return f"{self.user.name} has won {self.prize.prize}"

class ResetUserPassword(models.Model):
    """ResetUserPassword"""
    temp_pass = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    expiers_at= models.DateTimeField()
    is_active= models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    models.CheckConstraint(
        check=Q(expiers_at__gt=Now()),
        name = "expiers_at must be greater than or equal today"
    )
    
    def __str__(self):
        return f"{self.user.name} has an {'Active' if self.is_active else 'Inactive'} temp password of {self.temp_pass}"
      
