from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile

User = get_user_model()

@receiver(post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        client_group, _ = Group.objects.get_or_create(name='Clients')
        instance.groups.add(client_group)


@receiver(post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
