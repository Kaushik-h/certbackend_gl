# Generated by Django 3.1.7 on 2021-03-11 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.TextField(),
        ),
    ]