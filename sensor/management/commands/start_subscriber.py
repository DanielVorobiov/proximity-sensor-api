from django.core.management.base import BaseCommand

from sensor.tasks import start_subscriber


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Pub/Sub subscriber...'))
        start_subscriber()
        self.stdout.write(self.style.SUCCESS('Subscriber started successfully.'))