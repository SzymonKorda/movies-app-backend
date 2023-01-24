from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('movies', views.movie_list),
    path('movies/<int:movie_id>', views.movie_detail),
    path('movies/<int:movie_id>/actors/<int:actor_id>', views.movie_actors),
    path('actors', views.actor_list),
    path('actors/<int:actor_id>', views.actor_detail),
    path('actors/<int:actor_id>/movies/<int:movie_id>', views.actor_movies),
    path('auth/register', views.create_user),
    path('auth/login', jwt_views.TokenObtainPairView.as_view()),
    path('auth/refresh', jwt_views.TokenRefreshView.as_view()),
]
