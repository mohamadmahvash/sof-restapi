from rest_framework import serializers

from answers.models import Answer


class AnswersListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    question = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
