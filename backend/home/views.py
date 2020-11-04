from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Person, Score, Transaction
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthUserForm
from django.db import models
from django.contrib.auth.models import User


# Create your views here.
class List_persons(View):

    def get(self, request):
        current_url = request.get_full_path()
        scores = Score.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            persons = Person.objects.filter(
                (Q(full_name__contains=search_query) | Q(city__contains=search_query)) & ~Q(user_id=request.user.id))
        else:
            persons = Person.objects.exclude(user_id=request.user.id)
        paginator = Paginator(persons, 5)
        page_number = request.GET.get('page', '')
        page = paginator.get_page(page_number)

        if page.has_previous():
            prev_url = "?page={}".format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = "?page={}".format(page.next_page_number())
        else:
            next_url = ''

        context = {
            'persons': page,
            'scores': scores,
            'current_url': current_url,
            'prev_url': prev_url,
            'next_url': next_url
        }

        return render(request, 'home/home.html', context=context)


class LoginView(LoginView):
    template_name = 'home/authorization.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home_page_url')

    def get_success_url(self):
        return self.success_url


class LogoutView(LogoutView):
    next_page = reverse_lazy('home_page_url')


class Personal_accout(View):
    def get(self, request):
        person = Person.objects.get(user_id=request.user.id)
        scores = Score.objects.filter(person_score=person)
        current_url = request.get_full_path()
        search_query = request.GET.get('search', '')
        if search_query:
            transactions = Transaction.objects.filter(
                Q(write_of_score__number=search_query) | Q(deposit_score__number=search_query) | Q(deposit_score__person_score__full_name__contains = search_query))
        else:
            transactions = Transaction.objects.filter(Q(deposit_score__in=scores) | Q(write_of_score__in=scores))
        paginator = Paginator(transactions, 5)
        page_number = request.GET.get('page', '')
        page = paginator.get_page(page_number)
        if page.has_previous():
            prev_url = "?page={}".format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = "?page={}".format(page.next_page_number())
        else:
            next_url = ''
        context = {
            'person': person,
            'scores': scores,
            'transactions': page,
            'prev_url': prev_url,
            'next_url': next_url,
            'current_url': current_url
        }
        return render(request, 'home/personal_account.html', context=context)


class Score_detail(View):
    def get(self, request, slug):
        score = Score.objects.get(slug__iexact=slug)
        return render(request, 'home/score.html', context={'score': score})


class Transaction_detail(View):
    def get(self, request, slug):
        transaction = Transaction.objects.get(slug__iexact=slug)
        return render(request, 'home/transaction.html', context={'transaction': transaction})
