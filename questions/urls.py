from django.urls import path
from . import api_views

app_name = "questions"

urlpatterns = [
    path('', api_views.QuestionsListView.as_view(), name='questions_list'),
    path('<uuid:pk>/', api_views.QuestionDetailView.as_view(), name='question_detail'),
]
