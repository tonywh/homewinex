# Generated by Django 3.0.7 on 2020-08-12 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0015_auto_20200803_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='default_qty_kg_per_l',
            field=models.FloatField(default=0.2),
        ),
    ]
