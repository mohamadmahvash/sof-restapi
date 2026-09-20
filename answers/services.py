from django.db import transaction
from django.db.models import F

from .models import Answer
from questions.models import Question


@transaction.atomic
def create_answer(*, question, author, body):
    answer = Answer.objects.create(question=question, author=author, body=body)
    Question.objects.filter(id=question.id).update(answers_count=F('answers_count') + 1)
    return answer


@transaction.atomic
def delete_answer(*, answer):
    question_id = answer.question.id
    answer.delete()
    Question.objects.filter(id=question_id).update(answers_count=F('answers_count') - 1)
