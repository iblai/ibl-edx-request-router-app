"""
Signal handlers
"""
import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from .utils import manager_request


log = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def listen_for_user_creation(sender, instance, created, **kwargs):
    # Relay information to manager
    if created:
        manager_request('POST', '/core/users/proxy/', {
            'user_id': instance.id
        })
