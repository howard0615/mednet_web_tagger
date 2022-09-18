from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_situations, name='task_situations'),
    path('distribute_task/', views.distribute_task, name='distribute_task'),
    # path('assign_task', )
]