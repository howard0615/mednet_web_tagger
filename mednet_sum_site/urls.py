"""mednet_sum_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from .views import HomeView, upload_raw_json_data, download_raw_json_data


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'), # home.html設定
    path('accounts/', include('django.contrib.auth.urls')),
    path('questions/', include('question.urls')),
    path('task/', include('task.urls')),
    path('label/', include('labeling.urls')),
    path('labeltask/', include('labeltask.urls')),
    path('data/upload_file/', upload_raw_json_data, name='upload_raw_json_data'),#沒有寫在網頁裡 要自己打
    path('data/download_file/', download_raw_json_data, name='download_raw_json_data'),#沒有寫在網頁裡 要自己打
]
