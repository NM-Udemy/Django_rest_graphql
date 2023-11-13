import csv
from django.core.management.base import BaseCommand
from app.models import ToDo
from django.conf import settings
from os.path import join

class Command(BaseCommand):
    help = 'todo.csvを読み込んで挿入'
    
    def handle(self, *args, **kwargs):
        csv_file = join(settings.BASE_DIR, 'resources', 'todo.csv')
        
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ToDo.objects.create(
                    title=row['title'],
                    description=row['description'],
                    priority=int(row['priority']),
                    deadline=row['deadline'],
                    is_completed=row['is_completed'],
                    user_id=row['user_id'],
                )
        print('インポート終了')