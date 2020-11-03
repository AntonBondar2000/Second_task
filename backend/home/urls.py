from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', List_persons.as_view(), name='home_page_url'),
    path('authorization/', LoginView.as_view(), name='authorization_url'),
    path('logout/', LogoutView.as_view(), name = 'logout_url')
]