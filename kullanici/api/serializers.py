
from kullanici.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = ("first_name","last_name","password","email","il","ilce","phone","adres")
        lookup_field = 'email'
        extra_kwargs = {
            'url': {'lookup_field': 'email'}
        }

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)
