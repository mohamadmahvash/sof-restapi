from django.urls import path
from . import api_views

app_name = "questions"

urlpatterns = [
    path('', api_views.QuestionsListView.as_view()),
    path('<uuid:pk>/', api_views.QuestionDetailView.as_view()),
    path('create/', api_views.QuestionCreateView.as_view()),
    path('delete/<uuid:pk>/', api_views.QuestionDeleteView.as_view()),
    path('update/<uuid:pk>/', api_views.QuestionUpdateView.as_view()),
    path('accept/<uuid:question_id>/<uuid:answer_id>/', api_views.AcceptAnswerView.as_view()),
    path('deny/<uuid:question_id>/<uuid:answer_id>/', api_views.DenyAnswerView.as_view()),
]
