from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Person, Score
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AuthUserForm


# Create your views here.
class List_persons(View):

    def get(self, request):
        current_url = request.get_full_path()
        scores = Score.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            persons = Person.objects.filter(Q(full_name__contains=search_query) | Q(city__contains=search_query))
        else:
            persons = Person.objects.all()
        paginator = Paginator(persons, 2)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        if page.has_previous():
            prev_url = "?page={}".format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = "?page={}".format(page.next_page_number())
        else:
            next_url = ''

        return render(request, 'home/home.html',
                      context={'persons': page, 'scores': scores, 'current_url': current_url, 'prev_url': prev_url,
                               'next_url': next_url})


class LoginView(LoginView):
    template_name = 'home/authorization.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home_page_url')

    def get_success_url(self):
        return self.success_url


class LogoutView(LogoutView):
    next_page = reverse_lazy('home_page_url')
