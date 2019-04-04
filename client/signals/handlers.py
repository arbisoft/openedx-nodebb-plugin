from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from student.models import UserProfile
from openedx.features.openedx_nodebb_discussion.client.tasks import (
    task_create_user_on_nodebb, task_sync_user_profile_info_with_nodebb,
    task_delete_user_from_nodebb
)


@receiver(post_save, sender=User)
def create_and_update_user_on_nodebb(sender, instance, created, update_fields, **kwargs):
    if created:
        user_data = {
            'username': instance.username,
            'email': instance.email,
            'joindate': instance.date_joined.strftime("%s")
        }
        task_create_user_on_nodebb.delay(**user_data)
    elif update_fields is not None and 'last_login' not in update_fields:
        user_data = {
            'fullname': '{} {}'.format(instance.first_name, instance.last_name)
        }
        task_sync_user_profile_info_with_nodebb.delay(username=instance.username, **user_data)


@receiver(post_save, sender=UserProfile)
def sync_user_profile_info_with_nodebb(sender, instance, **kwargs):
    user = instance.user
    user_data = {
        'fullname': instance.name,
        'location': '{}, {}'.format(
            instance.city, instance.country.name),
        'birthday': '01/01/%s' % instance.year_of_birth
    }
    task_sync_user_profile_info_with_nodebb.delay(username=user.username, **user_data)


@receiver(pre_delete, sender=User)
def delete_user_from_nodebb(sender, instance, **kwargs):
    task_delete_user_from_nodebb.delay(username=instance.username)