from rest_framework import serializers

from .models import Question
from answers.serializers import AnswersListSerializer


class QuestionsListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    body = serializers.CharField()
    views_count = serializers.IntegerField()


class QuestionDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username')
    best_answer = AnswersListSerializer(read_only=True)

    class Meta:
        model = Question
        exclude = ['author']


class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()


class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'body']
