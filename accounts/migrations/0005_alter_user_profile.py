# Generated by Django 4.1.5 on 2023-02-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_user_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile",
            field=models.ImageField(
                default="avatar.svg", null=True, upload_to="profile_pictures"
            ),
        ),
    ]