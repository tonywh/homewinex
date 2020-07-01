# Generated by Django 3.0.7 on 2020-07-01 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_auto_20200626_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientuse',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='ingredientuse',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='visibility',
            field=models.PositiveSmallIntegerField(choices=[(0, 'private'), (1, 'public')], default=0),
        ),
    ]
