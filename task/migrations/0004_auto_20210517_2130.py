# Generated by Django 2.2.5 on 2021-05-17 21:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20210517_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='deadline',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]
