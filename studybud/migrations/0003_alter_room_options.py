# Generated by Django 4.1.3 on 2023-01-09 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studybud', '0002_topic_room_host_messages_room_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
