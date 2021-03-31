from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from .serializers import RegisterSerializer
from kullanici.models import User
from .permissions import NotAuthenticated
from rest_framework.response import Response
from time import time
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated

class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [NotAuthenticated,]
    lookup_field = 'email'
    lookup_value_regex = '[\w@.]+'
    # def put(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'email'
    lookup_value_regex = '[\w@.]+'
    permission_classes = [NotAuthenticated,]


class TestApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    # def put(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)