from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionsListSerializer, QuestionDetailSerializer, QuestionCreateSerializer, \
    QuestionUpdateSerializer
from .selectors import get_question_by_id, get_all_questions
from .services import create_question, increment_views_count, delete_question
from core.permissions import IsOwner


class QuestionsListView(APIView):
    def get(self, request):
        qs = get_all_questions()
        serialized_data = QuestionsListSerializer(instance=qs, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    def get(self, request, pk):
        qs = get_question_by_id(pk)
        serialized_data = QuestionDetailSerializer(instance=qs)
        increment_views_count(qs)
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


class QuestionDeleteView(APIView):
    permission_classes = [IsOwner]

    def delete(self, request, pk):
        qs = get_question_by_id(pk)
        self.check_object_permissions(request, qs)
        delete_question(qs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionUpdateView(APIView):
    permission_classes = [IsOwner]

    def patch(self, request, pk):
        qs = get_question_by_id(pk)
        self.check_object_permissions(request, qs)
        serializer = QuestionUpdateSerializer(instance=qs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialized_data = QuestionDetailSerializer(instance=qs)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
