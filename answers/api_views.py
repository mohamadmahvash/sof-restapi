from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsOwner
from questions.selectors import get_question_by_id
from .serializers import AnswersListSerializer


class AnswersListView(APIView):
    # permission_classes = [IsOwner]

    def get(self, request, question_id):
        question = get_question_by_id(q_id=question_id)
        answers = question.answers
        serializer = AnswersListSerializer(instance=answers, many=True)
        return Response(serializer.data)
