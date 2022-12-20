from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from .models import Film, Date, Times, Places, Ticket, Premier, Order
import requests
import json
import re
from datetime import date, time, timedelta, datetime
from .utils import CustDate, CustTime
from django.contrib.auth.views import LoginView
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from paypal.standard.forms import PayPalPaymentsForm

API_KEY = 'd0a52941-ee41-4d27-91a4-289f360ff1d6'
def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('notify')),
        "cancel_return": request.build_absolute_uri(reverse('places')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], email=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Пользователь заблокирован'})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def get_films(url):
    req = requests.get(url=url,
                       headers={
                           "Content-Type": "application/json",
                           "X-API-KEY": API_KEY
                       })
    data = json.loads(req.text)
    col = data['films'] if data.get('films') else data['items']
    films_ids = [item['filmId'] if item.get('filmId') else item['kinopoiskId'] for item in col]
    films = []
    for id in films_ids:
        req = requests.get(url=f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}',
                           headers={
                               "Content-Type": "application/json",
                               "X-API-KEY": API_KEY
                           }
                           )
        data = json.loads(req.text)
        film = dict()
        film['title'] = data.get('nameRu')
        film['description'] = data.get('description')
        film['image'] = data.get('posterUrl')
        film['rating'] = data.get('ratingKinopoisk') or 0
        film['year'] = data.get('year')
        film['type'] = ', '.join([x['genre'] for x in data['genres']])
        try:
            film['age_rating'] = re.findall(r'd+', str(data.get('ratingAgeLimits')))[0] + '+'
        except IndexError or TypeError:
            film['age_rating'] = '0+'
        film['country'] = ', '.join([x['country'] for x in data['countries']])
        films.append(film)
    return films


def load_places(time):
    for i in range(1, 11):
        place = Places(row=1, place=i, time=time, is_free=True)
        place.save()
    for i in range(1, 21):
        place = Places(row=2, place=i, time=time, is_free=True)
        place.save()
    for i in range(3, 12):
        for j in range(1, 31):
            place = Places(row=i, place=j, time=time, is_free=True)
            place.save()


def load_times(date):
    for i in range(9, 22, 3):
        ntime = time.fromisoformat(f'{i:02}:00:00')
        t = Times(time=ntime.strftime('%H:%M:%S'), date=date)
        t.save()
        load_places(t)


def load_dates(film):
    ndate = date.today()
    for i in range(7):
        dat = Date(date=ndate.strftime('%Y-%m-%d'), film=film)
        ndate = ndate + timedelta(days=1)
        dat.save()
        load_times(dat)




def load_films():
    films = get_films('https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page=1')
    for film in films:
        new_film = Film()
        new_film.title = film['title']
        new_film.description = film['description']
        new_film.image = film['image']
        new_film.rating = film['rating']
        new_film.premier_year = film['year']
        new_film.type = film['type']
        new_film.country = film['country']
        new_film.age_rating = film['age_rating']
        new_film.save()
        load_dates(new_film)

def load_premiers():
    films = get_films('https://kinopoiskapiunofficial.tech/api/v2.2/films/premieres?year=2022&month=DECEMBER')
    for film in films:
        new_film = Premier()
        new_film.title = film['title']
        new_film.description = film['description']
        new_film.image = film['image']
        new_film.rating = film['rating']
        new_film.premier_year = film['year']
        new_film.type = film['type']
        new_film.country = film['country']
        new_film.age_rating = film['age_rating']
        new_film.premier_month = 'декабрь'
        new_film.save()
        load_dates(new_film)

def index(request):
    films = Film.objects.all()
    return render(request, 'index.html', {'films': films})


def film_detail(request, film_id):
    film = Film.objects.get(id=film_id)
    dates = Date.objects.filter(film=film)
    dates = [CustDate(date) for date in dates]
    dates = {dates[i]: i * 70 for i in range(len(dates))}
    context = {
        'film': film,
        'dates': dates,
    }
    return render(request, 'films_detail.html', context)

def film_dated(request, film_id, date_id):
    film = Film.objects.get(id=film_id)
    dates = Date.objects.filter(film=film)
    dates = [CustDate(date) for date in dates]
    dates = {dates[i]: i * 70 for i in range(len(dates))}
    times = Times.objects.filter(date=date_id)
    times = [CustTime(time) for time in times]
    times = {times[i]: i * 70 for i in range(len(times))}
    context = {
        'film': film,
        'dates': dates,
        'times': times,
        'date_id': date_id
    }
    return render(request, 'film_dated.html', context)

def film_timed(request, film_id, date_id, time_id):
    film = Film.objects.get(id=film_id)
    dates = Date.objects.filter(film=film)
    dates = [CustDate(date) for date in dates]
    dates = {dates[i]: i * 70 for i in range(len(dates))}
    times = Times.objects.filter(date=date_id)
    times = [CustTime(time) for time in times]
    times = {times[i]: i * 70 for i in range(len(times))}
    context = {
        'film': film,
        'dates': dates,
        'times': times,
        'date_id': date_id,
        'time_id': time_id
    }
    return render(request, 'film_timed.html', context)

CHOSEN_PLACES = []

def places(request, film_id, time_id):
    items = Places.objects.filter(time=time_id)
    it = iter(items)
    items = [[next(it) for _ in range(10)], [next(it) for _ in range(20)]] +[[next(it) for i in range(30)] for j in range(3, 12)]
    items_dict = {}
    for i in range(1, len(items) + 1):
        items_dict[i] = items[i-1]

    context = {'film_id': film_id, 'time_id': time_id, 'places': items_dict, 'chosen_places': CHOSEN_PLACES}
    return render(request, 'places.html', context)

def choose(request, film_id, time_id, place_id):

    place = Places.objects.get(id=place_id)
    if place in CHOSEN_PLACES:
        CHOSEN_PLACES.remove(place)
    else:
        CHOSEN_PLACES.append(place)

    return redirect(places, film_id=film_id, time_id=time_id)


def pay(request, film_id, time_id):

    order = Order(user=request.user)
    amount = 0
    order.save()
    tickets = []
    for place in CHOSEN_PLACES:
        ticket = Ticket(order=order,
                        film=Film.objects.get(id=film_id),
                        time=Times.objects.get(id=time_id),
                        place=place,
                        )
        ticket.save()
        amount += ticket.price
        tickets.append(ticket)
    order.amount = amount
    order.save()


    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": f"{order.amount}",
        "item_name": "Билеты",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('notify', kwargs={'order_id':order.id})),
        "cancel_return": request.build_absolute_uri(reverse('index')),
        "custom": "premium_plan",
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, 'tickets': tickets, 'amount': amount}
    return render(request, "payment.html", context)

def notify(request, order_id):
    order = Order.objects.get(id=order_id)
    tickets = Ticket.objects.filter(order=order)
    for ticket in tickets:
        ticket.user = request.user
        ticket.order = None
        ticket.save()
    order.delete()

    return redirect(index)

def payment_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'payments.html', {'tickets': tickets})




def premiers(request):
    films = Premier.objects.all()
    return render(request, 'index.html', {'films': films})
