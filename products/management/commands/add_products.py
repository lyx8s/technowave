import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from products.models import product, category


class Command(BaseCommand):
    """Добавить товар в бд"""
    help = 'import data from csv'

    def handle(self, *args, **kwargs):
        path = Path(os.getcwd(), 'data', 'products.csv')
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file)
            products = [
                product.Product(
                    manufacturer=row[0].strip(),
                    model_name=row[1].strip(),
                    display_name=row[2].strip(),
                    code_model=row[3].strip(),
                    article_number=row[4].strip(),
                    description=row[5].strip(),
                    price=row[6].strip(),
                    subcategory=category.SubCategory.objects.get(
                        slug=row[7].strip()
                    ),
                )
                for row in reader
            ]
            product.Product.objects.bulk_create(products)
        print('Категории в базу данных загружены')
        print('ADD', product.Product.objects.count(), 'Products')
