# Generated by Django 5.0.3 on 2024-03-28 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summarize_app', '0003_alter_rating_comment_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summary_text',
            old_name='work_program_id',
            new_name='wp_id',
        ),
    ]