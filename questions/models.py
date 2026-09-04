from django.db import models
from core.models import BaseModel
from django.conf import settings


class Question(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    answers_count = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    best_answer = models.OneToOneField('answers.Answer', blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='best_answer')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

        indexes = [
            models.Index(fields=['title']),
        ]
