from rest_framework import serializers

from answers.models import Answer


class AnswersListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    question = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['body']

class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['body']