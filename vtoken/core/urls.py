from django.urls import path
from .views import (
    Test,
    CreateQuiz,
    CreateQuestion,
    AttemptQuiz,
    Result,
    RecordResponse,
    Attempt,
    DeleteQuestion,
    EditQuiz,
    EditQuestion,
    UserQuizRecord,
)

app_name = 'core'

urlpatterns = [
    path('test/', Test.as_view(), name='test'),
    path('create/', CreateQuiz.as_view(), name = 'create'),
    path('edit/<slug>/', EditQuiz.as_view(), name = 'edit_quiz'),

    path('<slug>/create/question/', CreateQuestion.as_view(), name = 'create_question'),
    path('question/<slug>/delete/<id>/', DeleteQuestion.as_view(), name = "delete_question"),
    path('question/<slug>/update/<id>/', EditQuestion.as_view(), name = "edit_question"),

    path('record/user/<slug>', UserQuizRecord.as_view(), name= 'user_quiz_record'),

    path('attempt/<slug>/', AttemptQuiz.as_view(), name = 'attempt_quiz'),
    path('attempt1/<slug>/<int:id>/<int:index>/', Attempt.as_view(), name = 'attempt'),

    path('result/<slug>/<id>/', Result.as_view(), name = 'quiz_result'),
    path('record_response/', RecordResponse.as_view(), name = 'ajax_record_response'),

]
