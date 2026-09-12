from django.core.management.base import BaseCommand
from django.db import transaction
from interface.factories import ALL_FACTORIES


class Command(BaseCommand):
    help = "Seeds database with generated fake dummy data using Factory Boy"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of records to create per model (default: 100)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.WARNING(f"Starting seed: Creating {count} records per model..."))

        for factory_cls in ALL_FACTORIES:
            model_name = factory_cls._meta.model.__name__
            factory_cls.create_batch(count)
            self.stdout.write(self.style.SUCCESS(f"✓ Created {count} records for {model_name}"))

        self.stdout.write(self.style.SUCCESS("\nDatabase seeding completed successfully!"))