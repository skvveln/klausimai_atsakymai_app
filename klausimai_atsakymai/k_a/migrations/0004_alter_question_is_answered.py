# Generated by Django 4.2.5 on 2023-09-09 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('k_a', '0003_rename_answered_question_is_answered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='is_answered',
            field=models.BooleanField(default=True),
        ),
    ]
