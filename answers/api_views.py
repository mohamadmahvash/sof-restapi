from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsOwner
from questions.selectors import get_question_by_id
from .selectors import get_answer_by_id
from .serializers import AnswersListSerializer, AnswerCreateSerializer, AnswerUpdateSerializer
from .services import create_answer, delete_answer


class AnswersListView(APIView):
    # permission_classes = [IsOwner]

    def get(self, request, question_id):
        question = get_question_by_id(q_id=question_id)
        answers = question.answers
        serializer = AnswersListSerializer(instance=answers, many=True)
        return Response(serializer.data)


class AnswerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = get_question_by_id(q_id=question_id)
        answer = create_answer(author=request.user, question=question, body=serializer.validated_data['body'])
        serializer_data = AnswersListSerializer(instance=answer)
        return Response(serializer_data.data, status=status.HTTP_201_CREATED)


class AnswerDeleteView(APIView):
    permission_classes = [IsOwner]

    def delete(self, request, answer_id):
        answer = get_answer_by_id(answer_id=answer_id)
        self.check_object_permissions(request, answer)
        delete_answer(answer=answer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerUpdateView(APIView):
    permission_classes = [IsOwner]

    def patch(self, request, answer_id):
        answer = get_answer_by_id(answer_id=answer_id)
        self.check_object_permissions(request, answer)
        serializer = AnswerUpdateSerializer(instance=answer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_data = AnswersListSerializer(instance=answer)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
