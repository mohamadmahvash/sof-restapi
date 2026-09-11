from .models import Question


def get_all_questions():
    return Question.objects.all()


def get_question_by_id(q_id):
    return Question.objects.filter(pk=q_id).first()
