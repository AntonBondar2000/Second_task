from django.shortcuts import render
from django.views.generic import View
from .models import Person, Score


# Create your views here.
class List_persons(View):
    persons = Person.objects.all()
    scores = Score.objects.all()

    def get(self, request):
        return render(request, 'home/home.html', context={'persons': self.persons, 'scores': self.scores})
