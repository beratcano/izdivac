# Generated by Django 5.1.6 on 2025-02-07 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='q_type',
            field=models.CharField(choices=[('multiple_choice_single', 'Multiple Choice Single'), ('multiple_choice_multiple', 'Multiple Choice Multiple'), ('open_ended', 'Open Ended')], default='open_ended', max_length=24),
        ),
    ]
