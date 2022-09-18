from django.urls import path
from . import views


urlpatterns = [
    path('', views.your_label_tasks, name='your_label_tasks'),
    path('do_label/<str:date>/', views.label_date_rough_see, name='label_date_rough_see'),
    path('do_label/<str:date>/<int:ques_id>/', views.do_label, name = 'do_label'),
    path('do_label/<str:date>/<int:ques_id>/next/<str:pure_next>/', views.next_data, name='label_next_data'),
    path('do_label/<str:date>/<int:ques_id>/prev/<str:pure_prev>/', views.prev_data, name='label_prev_data'),
    path('admin_review_labels/<int:ques_id>/', views.admin_review_labels, name='admin_review_labels'),   
    path('admin_review_labels/<int:ques_id>/next/<str:pure_next>/', views.next_review_data, name='admin_review_labels_next'),   
    path('admin_review_labels/<int:ques_id>/prev/<str:pure_prev>/', views.prev_review_data, name='admin_review_labels_prev'),   
]
