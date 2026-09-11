from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question
from .serializers import QuestionsListSerializer, QuestionDetailSerializer, QuestionCreateSerializer
from .selectors import *
from .services import *


class QuestionsListView(APIView):
    def get(self, request):
        questions = get_all_questions()
        serialized_data = QuestionsListSerializer(instance=questions, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    def get(self, request, pk):
        questions = get_question_by_id(pk)
        serialized_data = QuestionDetailSerializer(instance=questions)
        increment_views_count(questions)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = create_question(author=request.user, title=serializer.validated_data['title'],
                                   body=serializer.validated_data['body'])
        serialized_data = QuestionDetailSerializer(instance=question)
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
