from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question
from .serializers import QuestionsListSerializer, QuestionDetailSerializer


class QuestionsListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serialized_data = QuestionsListSerializer(instance=questions, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    def get(self, request, pk):
        questions = Question.objects.filter(id=pk).first()
        serialized_data = QuestionDetailSerializer(instance=questions)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
