# Generated by Django 4.2.5 on 2024-09-15 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_user_activity_user_avatar_user_connected_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='connections',
            new_name='num_connections',
        ),
        migrations.AddField(
            model_name='user',
            name='connected_users',
            field=models.ManyToManyField(blank=True, related_name='connected_to', to='students.user'),
        ),
    ]
