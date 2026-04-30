import random
from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Report

fake = Faker('id_ID')

class Command(BaseCommand):
    help = 'Generate fake reports data'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int)

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']

        categories = [
            'infra',
            'kebersihan',
            'lingkungan',
            'keamanan',
            'transportasi',
        ]

        status_choices = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']

        for _ in range(num_records):
            Report.objects.create(
                title=fake.sentence(nb_words=4),
                category=random.choice(categories),
                description=fake.text(),
                location=fake.city(),
                status=random.choice(status_choices),
            )

        self.stdout.write(self.style.SUCCESS(f'Berhasil membuat {num_records} data!'))