from django.db.models import F

from .models import Question


def create_question(*, author, title, body):
    return Question.objects.create(author=author, title=title, body=body)


def increment_views_count(question):
    question.views_count = F('views_count') + 1
    question.save()
