# Generated by Django 4.1.5 on 2023-02-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_bio_user_name_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile",
            field=models.ImageField(
                default="avatar.svg", null=True, upload_to="profile_pictures"
            ),
        ),
    ]
