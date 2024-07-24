from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from .models import UserConfirm
from .serializers import UserSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random


@api_view(['POST'])
def register_api_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        email=serializer.validated_data['email'],
        is_active=False
    )
    code = ''.join([str(random.randint(0, 9)) for i in range(6)])
    UserConfirm.objects.create(
        code=code,
        user=user
    )
    send_mail(
        'Your confirmation email',
        message=code,
        from_email='<EMAIL>',
        recipient_list=[user.email],
    )

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'User credentials are wrong'})


@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data['SMS']
    try:
        sms = UserConfirm.objects.get(code=code)
    except UserConfirm.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'error': 'code is invalid'})
    sms.user.is_active = True
    sms.user.save()
    sms.delete()
    return Response(status=status.HTTP_200_OK,
                    data={'active': True}
                    )
