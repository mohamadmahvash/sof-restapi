from django.shortcuts import get_object_or_404

from .models import Answer


def get_answer_by_id(*, answer_id):
    return get_object_or_404(Answer, pk=answer_id)

def get_answers_for_question(*, question):
    return Answer.objects.filter(question=question)
