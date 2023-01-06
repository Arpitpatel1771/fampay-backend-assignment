from django.urls import include,path
from Landingpage import views

urlpatterns = [
    path('list/', views.get_all_videos, name='get all videos'),
    path('search/', views.search_videos, name='search videos'),
]
