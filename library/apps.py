from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        from library.signals.categories import category_saved
        from library.signals.users import notify_admin_with_moderator_created
