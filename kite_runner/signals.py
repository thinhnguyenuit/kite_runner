from django.db.models.signals import post_save
from django.dispatch import receiver

from kite_runner.models import Profile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if instance and created:
        Profile.objects.create(user=instance)
