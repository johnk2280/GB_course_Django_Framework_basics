# Generated by Django 3.2.5 on 2021-09-02 13:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20210901_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 4, 13, 37, 2, 972464, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(default=18, verbose_name='возраст'),
        ),
    ]
