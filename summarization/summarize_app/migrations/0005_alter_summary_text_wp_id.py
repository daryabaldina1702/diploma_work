# Generated by Django 5.0.3 on 2024-03-28 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarize_app', '0004_rename_work_program_id_summary_text_wp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary_text',
            name='wp_id',
            field=models.ForeignKey(db_column='wp_id', on_delete=django.db.models.deletion.CASCADE, to='summarize_app.description'),
        ),
    ]
