from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('site/', views.site, name='site'),
    path('', views.index, name='index'),
    path('country/<int:id>/', views.country_detail, name='country_detail'),
    path('cities/', views.cities, name='cities'),
    path('search/', views.search, name='search'),  
    path('checkbook/', views.checkbook, name='checkbook'),
    path('contact/', views.contact, name='contact'),
    path("hotel/<int:id>/", views.hotel_detail, name="hotel_detail"),
    path("book-hotel/", views.book_hotel, name="book_hotel"),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('mybook/', views.mybook, name='mybook'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('hotel/<int:id>/comment/', views.add_comment, name='add_comment'),
]