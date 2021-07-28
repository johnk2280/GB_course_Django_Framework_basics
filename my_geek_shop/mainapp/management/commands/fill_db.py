import csv
import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from mainapp.models import ProductCategory, Product

CSV_PATH = 'mainapp/csv_files'
JSON_PATH = 'mainapp/json_files'


def load_from_csv(file_name):
    with open(os.path.join(CSV_PATH, file_name + '.csv'), 'r', encoding='utf-16') as f_obj:
        file_reader = csv.DictReader(f_obj)
        for row in file_reader:
            yield row


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as f_obj:
        return json.load(f_obj)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for category in categories['categories']:
            added_category = ProductCategory(**category)
            added_category.save()

        Product.objects.all().delete()
        for product in load_from_csv('products'):
            category_name = product['category']
            category_obj = ProductCategory.objects.get(name=category_name)
            product['category'] = category_obj
            added_product = Product(**product)
            added_product.save()

        super_user = User.objects.create_user(
            'Evgen',
            'Evgen@geekshop.local',
            'geekbrains',
        )
