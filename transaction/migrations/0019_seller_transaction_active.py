# Generated by Django 4.2.4 on 2023-09-10 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0018_remove_sell_difference_seller_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='transaction_active',
            field=models.BooleanField(default=True),
        ),
    ]
