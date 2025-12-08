from django.db.models.signals import post_save
from django.dispatch import receiver

from library.models import Category


@receiver(signal=post_save, sender=Category)
def category_saved(sender, instance: Category, created, **kwargs):
    if created:
        # Если created == True -- это создание объекта
        print(f"New category was created: Category name: {instance.name_category}")
    else:
        # Если мы попадём в else -- это обновление объекта
        print(f"The category was updated: Category name: {instance.name_category}")



# def category_saved(sender, instance, created, **kwargs):
#     if created:
#         print(f"New category was created: Category name: {instance.name}")
#     else:
#         print(f"The category was updated: Category name: {instance.name}")
#
#
#
# post_save.connect(category_saved, sender=Category)