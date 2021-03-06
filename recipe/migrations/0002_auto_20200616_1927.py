# Generated by Django 3.0.7 on 2020-06-16 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='ta',
            new_name='acid',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='yield_l',
            new_name='liquid',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='sg',
            new_name='sugar',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='body_to_acid',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='brownness',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='pectin',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='pectolaise',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='redness',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='solu_solid',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='starch',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='suggest_max',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unferm_sugar',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='variety',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='method',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='recipe.Method'),
            preserve_default=False,
        ),
    ]
