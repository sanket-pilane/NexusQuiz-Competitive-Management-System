
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import UserProfile

class Command(BaseCommand):
    help = 'Creates a default admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin@gmail.com').exists():
            user = User.objects.create_superuser('admin@gmail.com', 'admin@gmail.com', 'admin@123')
            UserProfile.objects.create(user=user, is_admin=True)
            self.stdout.write(self.style.SUCCESS('Successfully created admin user.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
