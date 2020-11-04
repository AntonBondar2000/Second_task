from django.contrib import admin
from .models import Person, Score, Transaction

admin.site.register(Person)
admin.site.register(Score)
admin.site.register(Transaction)