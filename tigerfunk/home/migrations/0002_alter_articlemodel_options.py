# Generated by Django 4.0.5 on 2022-06-17 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlemodel',
            options={'ordering': ['-date']},
        ),
    ]
