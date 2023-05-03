from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({"username": self.user.username})
        data.update({"is_admin": self.user.is_superuser})
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_admin"] = user.is_superuser
        return token
