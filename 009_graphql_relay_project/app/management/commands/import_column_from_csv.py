import csv
from django.core.management.base import BaseCommand
from app.models import Column
from django.conf import settings
from os.path import join

class Command(BaseCommand):
    help = 'columns.csvを読み込んで挿入'
    
    def handle(self, *args, **kwargs):
        csv_file = join(settings.BASE_DIR, 'resources', 'columns.csv')
        
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Column.objects.create(
                    title=row['title'],
                    description=row['description'],
                    user_id=row['user_id'],
                )
        print('インポート終了')
    