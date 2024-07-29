import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from products.models.category import SubCategory, Category


class Command(BaseCommand):
    """Добавить подкатегории товара в бд"""
    help = 'import data from csv'

    def handle(self, *args, **kwargs):
        path = Path(os.getcwd(), 'data', 'subcategory.csv')
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file)
            subcategory = [
                SubCategory(
                    name=row[0],
                    slug=row[1],
                    category=Category.objects.get(
                        slug=row[2].strip()
                    )
                )
                for row in reader
            ]
            SubCategory.objects.bulk_create(subcategory)
        print('Подкатегории в базу данных загружены')
        print('ADD', SubCategory.objects.count(), 'SubCategory')
