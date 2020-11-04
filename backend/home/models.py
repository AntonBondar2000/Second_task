from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def generation_slug(a):
    new_slug = slugify(a, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Person(models.Model):
    full_name = models.CharField(max_length=150, db_index=True, verbose_name="Полное имя")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                db_index=True, verbose_name="Информация о ползьзователе")
    date = models.DateField(blank=True, auto_now_add=False, verbose_name="Дата рождения")
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Телефон")
    email = models.CharField(max_length=50, db_index=True, verbose_name="Электронная почта")
    photo = models.ImageField(upload_to='Image', default="/Image/no_person.jpg", verbose_name="Фотография")
    city = models.CharField(max_length=50, blank=True, verbose_name="Город")
    adress = models.CharField(max_length=150, blank=True, verbose_name="Адресс")

    def __str__(self):
        return self.full_name


class Score(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    number = models.CharField(max_length=50, unique=True, verbose_name="Номер счета")
    money = models.PositiveIntegerField(default=0, verbose_name="Сумма")
    person_score = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Владелец")
    end_date = models.DateField(blank=True, auto_now_add=False, verbose_name="Дата окончания")
    currency = models.CharField(max_length=30, verbose_name="Валюта")
    bank = models.CharField(max_length=100, verbose_name="Банк")
    bic = models.CharField(max_length=50, verbose_name="БИК")
    inn = models.CharField(max_length=50, verbose_name="ИНН")
    kpp = models.CharField(max_length=50, verbose_name="КПП")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('score_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generation_slug(self.title)
        super().save(*args, **kwargs)


class Transaction(models.Model):
    write_of_score = models.OneToOneField(Score, on_delete=models.CASCADE, verbose_name="Счет списания",
                                          related_name="write_of")
    deposit_score = models.OneToOneField(Score, on_delete=models.CASCADE, verbose_name="Счет зачисления",
                                         related_name="deposit")
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    money = models.PositiveIntegerField(blank=True, verbose_name="Переведенная сумма")
    date = models.DateField(blank=True, auto_now=True, verbose_name="Дата окончания")

    def __str__(self):
        return "{} - транзакция".format(self.id)

    def get_absolute_url(self):
        return reverse('transaction_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generation_slug('transaction')
        super().save(*args, **kwargs)
