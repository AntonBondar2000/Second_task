from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from .forms import AuthUserForm
from .models import Person, Score, Transaction
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User

# Create your views here.
class List_persons(View):

    def get(self, request):
        current_url = request.get_full_path()
        scores = Score.objects.all()
        search_query = request.GET.get('search')
        if search_query:

            persons = Person.objects.filter(
                (Q(full_name__contains=search_query) | Q(city__contains=search_query)) & ~Q(user_id=request.user.id))
        else:
            persons = Person.objects.exclude(user_id=request.user.id)
        paginator = Paginator(persons, 5)
        page_number = request.GET.get('page', current_url)
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
        if request.user.is_authenticated:
            filter_query = request.GET.get('filter', '')
            person = Person.objects.get(user_id=request.user.id)
            scores = Score.objects.filter(person_score=person)
            current_url = request.get_full_path()
            search_query = request.GET.get('search', '')
            if search_query:
                transactions = Transaction.objects.filter(
                    Q(write_of_score__number=search_query) | Q(deposit_score__number=search_query) | Q(
                        deposit_score__person_score__full_name__contains=search_query))
            else:
                transactions = Transaction.objects.filter(Q(deposit_score__in=scores) | Q(write_of_score__in=scores))

            if filter_query:
                transactions = transactions.order_by(str(filter_query))

            paginator = Paginator(transactions, 10)
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
        else:
            url = reverse('home_page_url')
            response = HttpResponseRedirect(url)
            return response


class Score_detail(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            score = Score.objects.get(slug__iexact=slug)
            return render(request, 'home/score.html', context={'score': score})
        else:
            url = reverse('home_page_url')
            response = HttpResponseRedirect(url)
            return response


class Transaction_detail(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            transaction = Transaction.objects.get(slug__iexact=slug)
            return render(request, 'home/transaction.html', context={'transaction': transaction})
        else:
            url = reverse('home_page_url')
            response = HttpResponseRedirect(url)
            return response


class TransactionCreate(View):
    def get(self, request):
        if request.user.is_authenticated:
            dep_score = request.GET['deposit_score']
            user_scores = Score.objects.filter(person_score__user_id=request.user.id)
            dep_fullname = Score.objects.get(number__iexact=dep_score).person_score.full_name
            context = {
                'dep_score': dep_score,
                'user_scores': user_scores,
                'dep_fullname': dep_fullname
            }
            return render(request, 'home/transfer.html', context=context)
        else:
            url = reverse('home_page_url')
            response = HttpResponseRedirect(url)
            return response

    def post(self, request):

        deposit_score_post = request.POST['score_deposit']
        deposit_score = Score.objects.get(number__iexact=deposit_score_post)
        writeof_score_post = request.POST.getlist('writeoff[]')  # Номер счетов списани
        len_number_scores_all = len(writeof_score_post)
        transfer_money = int(request.POST['transfer_money'])

        if len_number_scores_all == 1:
            writeof_score = Score.objects.get(number__iexact=writeof_score_post[0])

            add_money_score = Score.objects.get(number__exact=deposit_score_post)
            add_money_score.money += transfer_money
            remove_money_score = Score.objects.get(number__exact=writeof_score_post[0])
            remove_money_score.money -= transfer_money
            add_money_score.save()
            remove_money_score.save()

            tr = Transaction()
            tr.write_of_score = writeof_score
            tr.deposit_score = deposit_score
            tr.money = transfer_money
            tr.save()

        elif len_number_scores_all > 1:
            ar_money = [0] * len_number_scores_all
            if transfer_money % len_number_scores_all == 0:
                for i in range(len_number_scores_all):
                    ar_money[i] = transfer_money / len_number_scores_all
            else:
                for i in range(len_number_scores_all):
                    if i == len_number_scores_all - 1:
                        ar_money[i] = transfer_money // len_number_scores_all + transfer_money % len_number_scores_all
                    else:
                        ar_money[i] = transfer_money // len_number_scores_all
            for ws, i in enumerate(writeof_score_post):
                ws = int(ws)
                writeof_score = Score.objects.get(number__iexact=writeof_score_post[ws])
                add_money_score = Score.objects.get(number__exact=deposit_score_post)
                add_money_score.money += ar_money[ws]
                remove_money_score = Score.objects.get(number__exact=writeof_score_post[ws])
                remove_money_score.money -= ar_money[ws]
                add_money_score.save()
                remove_money_score.save()

                tr = Transaction()
                tr.write_of_score = writeof_score
                tr.deposit_score = deposit_score
                tr.money = ar_money[ws]
                tr.save()
        else:
            return redirect('personal_account_url')
        return redirect('personal_account_url')


class TransactionCancel(View):
    def post(self, request):
        id_transaction = int(request.POST['id_transaction'])
        transaction = Transaction.objects.get(id=id_transaction)
        transaction_money = transaction.money
        deposit_number_score = transaction.deposit_score.number
        writeoff_number_score = transaction.write_of_score.number

        cancel_deposit_score = Score.objects.get(number__exact=deposit_number_score)
        cancel_deposit_score.money -= int(transaction_money)

        cancel_writeoff_score = Score.objects.get(number__exact=writeoff_number_score)
        cancel_writeoff_score.money += int(transaction_money)
        cancel_deposit_score.save()
        cancel_writeoff_score.save()
        transaction.delete()
        return redirect('personal_account_url')
