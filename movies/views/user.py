from typing import Dict

from django.http import JsonResponse, HttpRequest
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from movies.payload.user_create_request import UserCreateRequest
from movies.serializers.jwt_response import CustomTokenObtainPairSerializer
from movies.serializers.user import UserSerializer


class UserView(APIView):
    def post(self, request: HttpRequest) -> JsonResponse:
        user: ReturnDict = self.create_user(request)
        return JsonResponse({"data": user}, status=status.HTTP_201_CREATED)

    def create_user(self, request: HttpRequest) -> ReturnDict:
        user_data: Dict[str, UserCreateRequest] = JSONParser().parse(request)
        user_serializer: UserSerializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return user_serializer.data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
