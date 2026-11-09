from .models import Answer


def get_answer_by_id(*, answer_id):
    return Answer.objects.filter(id=answer_id).first()

def get_answers_for_question(*, question):
    return Answer.objects.filter(question=question)
