# Generated by Django 5.1.7 on 2025-03-23 16:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_messagetracker_messagetrackerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetracker',
            name='messageTrackerID',
            field=models.UUIDField(default=uuid.UUID('675470bf-c816-4015-b462-ad96ad6d4e25'), editable=False, primary_key=True, serialize=False),
        ),
    ]
