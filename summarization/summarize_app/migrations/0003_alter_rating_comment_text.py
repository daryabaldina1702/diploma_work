# Generated by Django 4.2.11 on 2024-03-28 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summarize_app', '0002_remove_summary_text_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comment_text',
            field=models.TextField(),
        ),
    ]