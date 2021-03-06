# Generated by Django 3.0.7 on 2020-07-27 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0013_auto_20200701_1043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logentry',
            options={'ordering': ['datetime']},
        ),
        migrations.RemoveField(
            model_name='logentry',
            name='parent',
        ),
        migrations.AddField(
            model_name='logentry',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='logs', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='liquid_large_units',
            field=models.PositiveSmallIntegerField(choices=[(0, 'L'), (1, 'ml'), (2, 'gal-US'), (3, 'gal-Imp'), (4, 'floz-US'), (5, 'floz-Imp')], default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='liquid_small_units',
            field=models.PositiveSmallIntegerField(choices=[(0, 'L'), (1, 'ml'), (2, 'gal-US'), (3, 'gal-Imp'), (4, 'floz-US'), (5, 'floz-Imp')], default=1),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateField()),
                ('text', models.TextField()),
                ('brew', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.Brew')),
                ('logEntry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.LogEntry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
    ]
