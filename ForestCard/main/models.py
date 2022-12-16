from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, null=True)
    image = models.ImageField(upload_to='films/')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    premier_year = models.SmallIntegerField()
    country = models.CharField(max_length=200, null=True)
    age_rating = models.CharField(max_length=5, null=True)
    type = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Date(models.Model):
    date = models.DateField()
    film = models.ForeignKey(Film, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date) + " " + str(self.film.title)


class Times(models.Model):
    date = models.ForeignKey(Date, on_delete=models.PROTECT)
    time = models.TimeField()

    def __str__(self):
        return str(self.time)


class Places(models.Model):
    row = models.IntegerField()
    place = models.IntegerField()
    is_free = models.BooleanField()
    time = models.ForeignKey(Times, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.row) + ' ' + str(self.place)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.PROTECT)
    time = models.ForeignKey(Times, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=8)
