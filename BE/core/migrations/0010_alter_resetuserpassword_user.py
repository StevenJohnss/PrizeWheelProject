# Generated by Django 3.2.18 on 2023-03-16 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_resetuserpassword_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetuserpassword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
