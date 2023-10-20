from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="CarGo API",
        default_version='v1',
        description="All cargo api endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hodzhakhov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include('main_app.urls')),
    path('api/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

urlpatterns += staticfiles_urlpatterns()