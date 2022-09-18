from django.urls import path
from . import views

urlpatterns = [
    path('', views.your_questions_task, name='your_questions_task'),
    path('total_question_numbers/', views.total_question_numbers, name='total_question_numbers'),
    path('more_undo_id/', views.more_undo_id, name='more_undo_id'),
    path('view/<int:ques_id>/', views.question_view, name='question_view'),
    path('do_summary/<str:date>/', views.date_rough_see, name='date_rough_see'),
    path('do_summary/<str:date>/<int:ques_id>/', views.do_summary, name = 'do_summary'),
    path('do_summary/<str:date>/<int:ques_id>/next/<str:pure_next>/', views.next_data, name='next_data'),
    path('do_summary/<str:date>/<int:ques_id>/prev/<str:pure_prev>/', views.prev_data, name='prev_data'),
    # path('do_summary/<int:ques_id>', views.do_summary),
]