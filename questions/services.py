from django.db.models import F
from rest_framework.exceptions import ValidationError

from .models import Question


def create_question(*, author, title, body):
    return Question.objects.create(author=author, title=title, body=body)


def increment_views_count(question):
    question.views_count = F('views_count') + 1
    question.save()


def delete_question(question):
    question.delete()


def accept_answer(*, question, answer):
    if question.id != answer.question.id:
        raise ValidationError("Answer doesn't belong to this question")
    if question.best_answer or answer.is_best:
        raise ValidationError("Answer has already been accepted")

    question.best_answer = answer
    question.save(update_fields=['best_answer'])
    answer.is_best = True
    answer.save(update_fields=['is_best'])
    return question

def denied_answer(*, question, answer):
    if question.id != answer.question.id:
        raise ValidationError("Answer doesn't belong to this question")
    if not question.best_answer or not answer.is_best:
        raise ValidationError("Answer has already been accepted")
    question.best_answer = None
    question.save(update_fields=['best_answer'])
    answer.is_best = False
    answer.save(update_fields=['is_best'])
