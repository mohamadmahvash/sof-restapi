from django.urls import path
from . import api_views

app_name = "questions"

urlpatterns = [
    path('', api_views.QuestionsListView.as_view()),
    path('<uuid:pk>/', api_views.QuestionDetailView.as_view()),
    path('create/', api_views.QuestionCreateView.as_view()),
]
