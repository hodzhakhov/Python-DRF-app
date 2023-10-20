from djongo import models
from django_jsonform.models.fields import JSONField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.http.response import HttpResponseBadRequest


class UserManager(BaseUserManager):
    def create_user(self, username, email, role, is_organization, password=None):
        if username is None:
            return HttpResponseBadRequest('Users must have a username.')

        if email is None:
            return HttpResponseBadRequest('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), role=role,
                          is_organization=is_organization)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            return HttpResponseBadRequest('Superusers must have a password.')

        user = self.create_user(username, email, 'D', False, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('P', 'Перевозчик'),
        ('D', 'Диспетчер'),
        ('G', 'Грузовладелец'),
    )
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    role = models.CharField(max_length=10, choices=ROLES)
    is_organization = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        refresh = RefreshToken.for_user(self)

        return str(refresh.access_token)


class Order(models.Model):
    STOPS_SCHEMA = {
        'type': 'array',
        'items': {
            'type': 'string'
        }
    }

    city_from = models.CharField(max_length=100, default='')
    city_to = models.CharField(max_length=100, default='')
    stops = JSONField(schema=STOPS_SCHEMA, blank=True)
    container_type = models.CharField(max_length=100, default='')
    cargo_type = models.CharField(max_length=100, default='')
    temperature_regime = models.CharField(max_length=100, default='')
    cargo_readiness = models.BooleanField(default=False)
    loading_type = models.CharField(max_length=100, default='')
    weight = models.IntegerField()
    volume = models.IntegerField()
    trucks_number = models.IntegerField()
    currency = models.CharField(max_length=50, default='')
    rate = models.IntegerField()
    prepayment = models.IntegerField()
    special_requirements = models.CharField(max_length=200, default='')
    loading_date = models.DateField()
    date = models.DateField(auto_now=True)
    phone_number = models.CharField(max_length=100, default='')
    note = models.CharField(max_length=500, default='')
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)


class Transport(models.Model):
    container_type = models.CharField(max_length=100, default='')
    loading_type = models.CharField(max_length=100, default='')
    weight = models.IntegerField()
    volume = models.IntegerField()
    registration_number = models.CharField(max_length=100, default='')
    is_available = models.BooleanField(default=False)
    temperature_regime = models.CharField(max_length=100, default='')
    brand = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, related_name='transports', on_delete=models.CASCADE)


class Review(models.Model):
    note = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    performer = models.ForeignKey(User, related_name='performer', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE, blank=True)
    rating = models.IntegerField(default=0, blank=True)
    created = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created',)
