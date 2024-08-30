from django.core.management.base import BaseCommand, CommandError
import json

from item.models import Item


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        try:
            with open(options["file_path"], "r", encoding="utf-8") as file:
                items_data = json.load(file)
                items = [
                    Item(
                        name=item["name"],
                        description=item["description"],
                        price=item["price"],
                    )
                    for item in items_data
                ]
                Item.objects.bulk_create(items)
        except Exception:
            raise CommandError("Error when creating Items")
        self.stdout.write(self.style.SUCCESS("Items created"))
