# Generated by Django 4.1.4 on 2022-12-16 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_date_places_times_ticket_places_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=8, max_digits=4),
        ),
    ]
