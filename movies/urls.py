from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('movies', views.MovieView.as_view()),
    path('movies/<int:movie_id>', views.MovieView.as_view()),
    path('movies/<int:movie_id>/actors/<int:actor_id>', views.MovieActorsView.as_view()),
    path('actors', views.ActorView.as_view()),
    path('actors/<int:actor_id>', views.ActorView.as_view()),
    path('actors/<int:actor_id>/movies/<int:movie_id>', views.ActorMoviesView.as_view()),
    path('auth/register', views.UserView.as_view()),
    path('auth/login', views.CustomTokenObtainPairView.as_view()),
    path('auth/refresh', jwt_views.TokenRefreshView.as_view()),
]
