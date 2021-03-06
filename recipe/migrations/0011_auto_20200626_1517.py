# Generated by Django 3.0.7 on 2020-06-26 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_auto_20200625_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='visibility',
            field=models.PositiveSmallIntegerField(choices=[(0, 'priivate'), (1, 'public')], default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='create_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
