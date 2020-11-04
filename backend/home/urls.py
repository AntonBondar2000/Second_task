from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', List_persons.as_view(), name='home_page_url'),
    path('personal_account/', Personal_accout.as_view(), name='personal_account_url'),
    path('personal_account/score/<str:slug>/', Score_detail.as_view(), name='score_detail_url'),
    path('personal_account/transaction/create/', TransactionCreate.as_view(), name='transaction_create_url'),
    path('personal_account/transaction/delete/', TransactionCancel.as_view(), name='transaction_cancel_url'),
    path('personal_account/transaction/<str:slug>/', Transaction_detail.as_view(), name='transaction_detail_url'),
    path('authorization/', LoginView.as_view(), name='authorization_url'),
    path('logout/', LogoutView.as_view(), name='logout_url')
]
