import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from products.models import category


class Command(BaseCommand):
    """Добавить категории товара в бд"""
    help = 'import data from csv'

    def handle(self, *args, **kwargs):
        path = Path(os.getcwd(), 'data', 'category.csv')
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file)
            category_data = [
                category.Category(
                    name=row[0].strip(),
                    slug=row[1].strip()
                )
                for row in reader
            ]
            category.Category.objects.bulk_create(category_data)
        print('Категории в базу данных загружены')
        print('ADD', category.Category.objects.count(), 'Category')
