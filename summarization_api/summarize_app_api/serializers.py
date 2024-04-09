from rest_framework import serializers
from .models import Description, Summary_text, Rating, Editor


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['work_program_id', 'description_text']


class SummaryTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary_text
        fields = ['summarization_id', 'summarize_text', 'wp_id']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating_id', 'rating_score', 'comment_text', 'author', 'summarization_id']


class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = ['username', 'last_name', 'first_name', 'email', 'work_program_id']
