# Generated by Django 4.2.11 on 2024-03-28 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarize_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summary_text',
            name='id',
        ),
        migrations.AlterField(
            model_name='summary_text',
            name='summarization_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='summary_text',
            name='summirize_text',
            field=models.TextField(),
        ),
    ]
