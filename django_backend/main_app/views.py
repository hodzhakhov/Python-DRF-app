from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, CreateAPIView
import json

from main_app.models import Order, User, Transport, Review
from main_app.serializers import (
    OrderShowSerializer, OrderCreateSerializer, SignupSerializer, LoginSerializer, UserSerializer, AllUsersSerializer,
    TransportShowSerializer, TransportCreateSerializer, ReviewShowSerializer, ReviewCreateSerializer
)

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from django_telegram_login.widgets.constants import (
    SMALL,
    MEDIUM,
    LARGE,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN


def profile(request):
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')

    try:
        result = verify_telegram_authentication(bot_token=bot_token, request_data=request.GET)

    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')

    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')

    # Or handle it as you wish. For instance, save to the database.
    return HttpResponse('Hello, ' + result['username'] + '!')


class OrdersList(ListAPIView):
    serializer_class = OrderShowSerializer

    def get_queryset(self):
        order = Order.objects.all()
        str_filters = self.request.GET.get('filter', None)
        if str_filters is not None:
            json_filter = json.loads(str_filters)
            for i, j in json_filter.items():
                order = order.filter(**{i: j})
        return order


class OrderCreate(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OneOrder(RetrieveUpdateAPIView):
    serializer_class = OrderShowSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        serializer_data = JSONParser().parse(request)

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrder(DestroyAPIView):
    serializer_class = OrderShowSerializer
    queryset = Order.objects.all()


class TransportsList(ListAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportShowSerializer


class TransportCreate(CreateAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OneTransport(RetrieveUpdateAPIView):
    serializer_class = TransportShowSerializer
    queryset = Transport.objects.all()

    def update(self, request, *args, **kwargs):
        serializer_data = JSONParser().parse(request)

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteTransport(DestroyAPIView):
    serializer_class = TransportShowSerializer
    queryset = Transport.objects.all()


class ReviewsList(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewShowSerializer


class ReviewCreate(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Signup(CreateAPIView):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    user = JSONParser().parse(request)
    login_serializer = LoginSerializer(data=user)
    login_serializer.is_valid(raise_exception=True)

    return Response(login_serializer.validated_data, status=status.HTTP_200_OK)


class UsersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = AllUsersSerializer
    permission_classes = [IsAdminUser]


class OneUser(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
