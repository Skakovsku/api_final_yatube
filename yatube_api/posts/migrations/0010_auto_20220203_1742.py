# Generated by Django 2.2.16 on 2022-02-03 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20220203_1732'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='following_uniq',
        ),
    ]