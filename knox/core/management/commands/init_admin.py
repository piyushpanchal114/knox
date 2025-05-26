from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Command to initiate Super User"

    def handle(self, *args, **options):
        if User.objects.count() < 1:
            User.objects.create_superuser(
                username="admin", email="admin@admin.com", password="admin")
            msg = "Super User created successfully..." +\
                " \U0001F44D\U0001F44D\U0001F44D"
            self.stdout.write(self.style.SUCCESS(msg))
        else:
            msg = "User already exists... \U0001F44F\U0001F44F\U0001F44F"
            self.stdout.write(
                self.style.NOTICE(msg))
