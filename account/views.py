from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,  LoginSerializer
User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data # тело запроса
        serializer = UserSerializer(data=data) # переводим в питон  формат
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Пользователь успешно зарегистрирован', status=201)


class ActivationView(APIView):
    def get(self, request):
        data = request.data

        activation_code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Аккаунт успешно активирован', status=200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно вышли из аккаунта', status=200)


class ResetPasswordView(APIView):
    pass


class ChangePasswordView(APIView):
    pass

