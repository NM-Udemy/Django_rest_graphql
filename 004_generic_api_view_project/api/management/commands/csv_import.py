from django.core.management.base import BaseCommand
from pathlib import Path
from os.path import join
import csv
from api.models import Post, Comment
from django.contrib.auth.models import User


class Command(BaseCommand):
    
    def bulk_create_from_csv(self, model, csv_path):
        with open(csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            data_list = []
            for row in reader:
                model_instance = model(**row)
                if model == User:
                    model_instance.set_password('12345678')
                data_list.append(model_instance)
            model.objects.bulk_create(data_list)
    
    def handle(self, *args, **options):
        current_dir_path = Path(__file__).resolve().parent
        current_dir_path = join(current_dir_path, 'csvs')
        csv_file_list = ["users.csv", "posts.csv", "comments.csv"]
        model_list = [User, Post, Comment]
        for csv_file, model in zip(csv_file_list, model_list):
            csv_path = join(current_dir_path, csv_file)
            self.bulk_create_from_csv(model, csv_path)
        
    