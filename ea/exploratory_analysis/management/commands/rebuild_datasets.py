from django.core.management.base import BaseCommand, CommandError
from exploratory_analysis.models import Dataset
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = 'Rebuild all datasets that need it using output_viewer.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action="store_true")

    def handle(self, *args, **options):
        datasets = Dataset.objects.all()
        now = timezone.now()
        for ds in datasets:
            # Since rebuild() takes a little while, we'll make sure that the dataset is fresh
            try:
                ds = Dataset.objects.get(id=ds.id)
            except Dataset.DoesNotExist:
                # Dataset must have been deleted... not our problem anymore!
                continue
            if not options["force"]:
                if ds.should_rebuild is not None:
                    if ds.should_rebuild > now:
                        continue
            ds.rebuild()
            ds.should_rebuild = timezone.now() + datetime.timedelta(7)
            ds.save()
