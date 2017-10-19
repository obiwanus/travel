from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User as DjangoUser
from django.dispatch import receiver


class User(DjangoUser):
    class Meta:
        proxy = True

    @property
    def role(self):
        return self.profile.role


class UserProfile(models.Model):
    USER = 'Normal user'
    USER_MANAGER = 'User manager'
    ADMIN = 'Administrator'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',
                                on_delete=models.CASCADE)
    role = models.CharField(max_length=15, default=USER, choices=(
        (USER, 'Normal user'),
        (USER_MANAGER, 'User manager'),
        (ADMIN, 'Administrator'),
    ))

    def __str__(self):
        return self.user.email

    def is_admin(self):
        return self.role == self.ADMIN


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


