# Generated by Django 4.2.15 on 2024-08-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0003_alter_item_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="название"
            ),
        ),
    ]
