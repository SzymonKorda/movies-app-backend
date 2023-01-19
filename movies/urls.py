from django.urls import path

from . import views


urlpatterns = [
    path('movies', views.get_movie_list),
    path('movies', views.create_movie),
    path('movies/<int:movie_id>', views.get_movie),
]
