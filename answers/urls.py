from django.urls import path
from . import api_views

app_name = "answers"

urlpatterns = [
    path("<uuid:question_id>/", api_views.AnswersListView.as_view()),
    path("create/<uuid:question_id>/", api_views.AnswerCreateView.as_view()),
    path("delete/<uuid:answer_id>/", api_views.AnswerDeleteView.as_view()),
    path("update/<uuid:answer_id>/", api_views.AnswerUpdateView.as_view()),
]
