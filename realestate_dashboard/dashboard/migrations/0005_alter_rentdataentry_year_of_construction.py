# Generated by Django 4.2.7 on 2023-11-05 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0004_remove_rentdataentry_number_of_rooms_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rentdataentry",
            name="year_of_construction",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
