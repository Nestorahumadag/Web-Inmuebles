# Generated by Django 5.0.7 on 2024-07-30 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0007_remove_inmueble_tipo_inmueble_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comuna",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="web.region"
            ),
        ),
    ]
