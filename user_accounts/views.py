from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, GenericAPIView
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, UserImageSerializer, RefreshTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# register api view
class RegisterView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# login api view
@api_view(['POST'])
def loginView(request):
    context = {
        'done': {},
        'error': {}
    }

    if not request.data:
        msg = 'request cant be empty'
        context['error']['request'] = msg
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    # strip => to remove whitespaces from the leading and end of the string
    email = request.data['email'].strip()
    password = request.data['password'].strip()

    if email == "" and password == "":
        msg = 'this field is required'
        context['error']['email'] = msg
        context['error']['password'] = msg
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    if not User.objects.filter(email=email).exists():
        msg = 'email not found'
        context['error']['email'] = msg
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    if not user:
        msg = 'wrong password'
        context['error']['password'] = msg
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    login(request, user=user)

    profile_img = UserImageSerializer(user, context={"request": request})

    token = get_tokens_for_user(user)
    context['done']['token'] = token
    context['done']['user'] = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile_img': profile_img.data.get('profile_img')
    }

    return Response(context, status=status.HTTP_202_ACCEPTED)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetUserData(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
