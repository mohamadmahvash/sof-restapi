from django.shortcuts import get_object_or_404

from .models import Question


def get_all_questions():
    return Question.objects.all()


def get_question_by_id(q_id):
    return get_object_or_404(Question, pk=q_id)
