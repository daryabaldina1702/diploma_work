from django.db import models


class Description(models.Model):
    work_program_id = models.IntegerField(primary_key = True)
    description_text = models.TextField()

class Editor(models.Model):
    username = models.IntegerField(primary_key = True)
    last_name = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    work_program_id = models.ForeignKey(Description, on_delete = models.CASCADE)

class Summary_text(models.Model):
    summarization_id = models.AutoField(primary_key=True)
    summirize_text = models.TextField()
    wp_id = models.ForeignKey(Description, on_delete = models.CASCADE, db_column='wp_id')


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating_score = models.BooleanField()
    comment_text = models.TextField()
    author = models.CharField(max_length = 100)
    summarization_id = models.ForeignKey(Summary_text, on_delete = models.CASCADE)