from django.db import models
from django.conf import settings
from core.models import BaseModel


class Answer(BaseModel):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    is_best = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Answer: #{self.pk}'

    class Meta:
        ordering = ['-is_best', '-score', '-created']
