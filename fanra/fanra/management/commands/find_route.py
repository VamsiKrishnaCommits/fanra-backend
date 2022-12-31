from django.core.management.base import BaseCommand
from fanra.relations import *


class Command(BaseCommand):
    help = "populates the tables with configurations required for notifications"

    def handle(self, *args, **options):
        l = populate("11636", "11690")
        result = ""
        for i in l:
            result += str(i.name) + "-->"
        self.stdout.write(self.style.SUCCESS(result))
