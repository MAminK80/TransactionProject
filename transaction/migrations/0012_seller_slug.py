# Generated by Django 4.2.4 on 2023-08-29 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_transaction_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]