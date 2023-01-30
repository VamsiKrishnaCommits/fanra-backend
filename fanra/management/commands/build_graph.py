from django.core.management.base import BaseCommand
from fanra.djikstra import build_graph

class Command(BaseCommand):
    help = "Rebuild the graph data structure"

    def handle(self, *args, **options):
        build_graph(force=True )
        self.stdout.write(self.style.SUCCESS("Graph rebuilt successfully!"))
