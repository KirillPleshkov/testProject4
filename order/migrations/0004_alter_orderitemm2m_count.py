# Generated by Django 4.2.15 on 2024-08-31 05:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_orderitemm2m_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitemm2m",
            name="count",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="количество",
            ),
        ),
    ]
