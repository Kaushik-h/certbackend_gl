# Generated by Django 3.1.7 on 2021-03-09 13:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20210309_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiztaker',
            name='max_score',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quiztaker',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 9, 13, 38, 38, 22086)),
        ),
    ]
