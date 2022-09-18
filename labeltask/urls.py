from django.urls import path
from . import views

urlpatterns = [
    path('',views.label_task_situations, name = 'label_task_situations'),
    path('distribute_label_task/', views.distribute_label_task, name='distribute_label_task')
]