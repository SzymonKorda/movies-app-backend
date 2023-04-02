from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views.actor import *
from .views.movie import *
from .views.user import *

urlpatterns = [
    path('movies', MovieView.as_view()),
    path('movies/<int:movie_id>', MovieView.as_view()),
    path('movies/<int:movie_id>/actors', MovieActorsView.as_view()),
    path('movies/<int:movie_id>/actors/<int:actor_id>', MovieActorsView.as_view()),
    path('movies/<int:movie_id>/genres', MovieGenresView.as_view()),
    path('actors', ActorView.as_view()),
    path('actors/<int:actor_id>', ActorView.as_view()),
    path('actors/<int:actor_id>/movies', ActorMoviesView.as_view()),
    path('actors/<int:actor_id>/movies/<int:movie_id>', ActorMoviesView.as_view()),
    path('auth/register', UserView.as_view()),
    path('auth/login', CustomTokenObtainPairView.as_view()),
    path('auth/refresh', jwt_views.TokenRefreshView.as_view()),
]
