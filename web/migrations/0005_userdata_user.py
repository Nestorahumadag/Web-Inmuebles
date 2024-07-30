# Generated by Django 5.0.7 on 2024-07-29 21:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0004_inmueble_imagen"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userdata",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_data",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
