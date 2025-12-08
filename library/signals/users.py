from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from library.enums import Role
from library.models import User


@receiver(post_save, sender=User)
def notify_admin_with_moderator_created(sender, instance: User, created, **kwargs):
    if created and instance.is_staff and instance.role == Role.moderator.lower():

        send_mail(
            subject="New Moderator",
            message=f"New moderator {instance.username} was added to the library. You can contact with him by his email address: '{instance.email}'",
            from_email="no-reply.250425_library@gmail.com",
            recipient_list=["admin.core@gmail.com"],
            fail_silently=False
        )
