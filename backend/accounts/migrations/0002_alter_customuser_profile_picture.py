# Generated by Django 5.1.4 on 2024-12-22 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="profile_pics/default.jpg",
                null=True,
                upload_to="profile_pics/",
            ),
        ),
    ]