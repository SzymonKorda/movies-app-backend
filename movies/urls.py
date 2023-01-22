from django.urls import path

from . import views

urlpatterns = [
    path('movies', views.movie_list),
    path('movies/<int:movie_id>', views.movie_detail),
    path('movies/<int:movie_id>/actors/<int:actor_id>', views.movie_actors),
    path('actors', views.actor_list),
    path('actors/<int:actor_id>', views.actor_detail),
    path('actors/<int:actor_id>/movies/<int:movie_id>', views.actor_movies),
]
