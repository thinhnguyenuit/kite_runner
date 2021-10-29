# Generated by Django 3.2.7 on 2021-10-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kite_runner', '0003_article_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favourites',
            field=models.ManyToManyField(related_name='favourited_by', to='kite_runner.Article'),
        ),
    ]
