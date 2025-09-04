from django.apps import AppConfig
import os

class AgriTechAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agriTechApp'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Only create if no superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
            email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
            first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "")
            last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "")

            if username and email and password:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
