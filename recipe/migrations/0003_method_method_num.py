# Generated by Django 3.0.7 on 2020-06-17 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_auto_20200616_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='method_num',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
