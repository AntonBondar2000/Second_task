from django.db import models


class Person(models.Model):
    full_name = models.CharField(max_length=150, db_index=True, verbose_name="Полное имя")
    date = models.DateField(blank=True, auto_now_add=False, verbose_name="Дата рождения")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.CharField(max_length=50, db_index=True, verbose_name="Электронная почта")
    photo = models.ImageField(upload_to='Image', verbose_name="Фотография")
    city = models.CharField(max_length=50,blank=True, verbose_name="Город")

    def __str__(self):
        return self.full_name


class Score(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="Название")
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