from .models import Answer


def get_answer_by_id(*, answer_id):
    return Answer.objects.filter(id=answer_id).first()
