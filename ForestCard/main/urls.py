from django.urls import path
from .views import index, film_detail, film_dated,\
                   film_timed, places, choose, user_login,\
                   register, notify, payment_list, pay, premiers
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('film/<int:film_id>/', film_detail, name='film_detail'),
    path('film/<int:film_id>/<int:date_id>', film_dated, name='film_dated'),
    path('film/<int:film_id>/<int:date_id>-<int:time_id>', film_timed, name='film_timed'),
    path('film/<int:film_id>/places/<int:time_id>', places, name='places'),
    path('film/<int:film_id>/places/<int:time_id>/<int:place_id>', choose, name='choose_place'),
    path('login/', user_login, name='login'),
    path('registration/', register, name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('notify/<int:order_id>', notify, name='notify'),
    path('user/payments/', payment_list, name='payments'),
    path('film/<int:film_id>/<int:time_id>/pay', pay, name='pay'),
    path('premiers/', premiers, name='premiers')
]