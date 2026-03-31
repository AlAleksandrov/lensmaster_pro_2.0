from django.contrib.auth import get_user_model
from django.db import models
from common.models import ContactInfoMixin

User = get_user_model()

# Create your models here.
class Profile(ContactInfoMixin, models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    favorite_productions = models.ManyToManyField(
        'productions.Production',
        related_name='favorite_by',
        blank=True,
    )
    favorite_equipment = models.ManyToManyField(
        'inventory.Equipment',
        related_name='favorite_by',
        blank=True,
    )
    favorite_packages = models.ManyToManyField(
        'bookings.ServicePackage',
        related_name='favorite_by',
        blank=True,
    )

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f'Profile of {self.user.get_full_name() or self.user.username}'