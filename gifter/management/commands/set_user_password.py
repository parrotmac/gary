from django.core.management import BaseCommand

from gifter.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str, nargs="?")

    def handle(self, *args, **options):
        email = options.get("email")
        if not email:
            raise Exception("Must specify 'email'")

        user = User.objects.get(email=email)
        password = options.get("password")
        if not password:
            password = input(f"Please enter a new password for {email}: ")
        user.set_password(password)
        user.save()
        print("Updated!")
