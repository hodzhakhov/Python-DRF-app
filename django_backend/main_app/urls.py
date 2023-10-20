from django.urls import re_path
from django.views.generic import TemplateView
from main_app import views

urlpatterns = [
    re_path(r'order$', views.OrderCreate.as_view()),
    re_path(r'orders$', views.OrdersList.as_view()),
    re_path(r'^order/(?P<pk>[0-9]+)$', views.OneOrder.as_view()),
    re_path(r'^order/delete/(?P<pk>[0-9]+)$', views.DeleteOrder.as_view()),
    re_path(r'transport$', views.TransportCreate.as_view()),
    re_path(r'transports$', views.TransportsList.as_view()),
    re_path(r'^transport/(?P<pk>[0-9]+)$', views.OneTransport.as_view()),
    re_path(r'^transport/delete/(?P<pk>[0-9]+)$', views.DeleteTransport.as_view()),
    re_path(r'review$', views.ReviewCreate.as_view()),
    re_path(r'reviews$', views.ReviewsList.as_view()),
    re_path(r'^signup$', views.Signup.as_view()),
    re_path(r'^login$', views.login),
    re_path(r'^user$', views.OneUser.as_view()),
    re_path(r'^users$', views.UsersList.as_view()),
    re_path(r'^logintg$', TemplateView.as_view(template_name='login.html')),
    re_path(r'profile$', views.profile)
]
