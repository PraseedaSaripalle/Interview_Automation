# Generated by Django 3.2.9 on 2022-04-13 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentenceCheck', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='parents', to='sentenceCheck.Topic'),
        ),
    ]