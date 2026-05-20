from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.cache import never_cache

from .models import Hotel, Booking, Contact, HotelComment, Country

def site (request):
    return render(request, 'members/site.html')

@never_cache
def index(request):
    hotels = Hotel.objects.all()
    countries = Country.objects.all()
    bookings = Booking.objects.all().order_by('-id')

    # Get hotels where the related country name is 'India'
    india_hotels = Hotel.objects.filter(country__country__iexact="India")[:7]
    dubai_hotels = Hotel.objects.filter(country__country__iexact="Dubai")[:7]
    france_hotels = Hotel.objects.filter(country__country__iexact="France")[:7]
    
    return render(request, 'members/index.html', {
        'hotels': hotels,
        'bookings': bookings,
        'india_hotels': india_hotels,
        'countries': countries,
        'dubai_hotels': dubai_hotels,
        'france_hotels': france_hotels, 
    })

#   explore countries
def country_detail(request, id):
    country_item = get_object_or_404(Country, id=id)
    hotels =  Hotel.objects.filter(country=country_item)
    return render(request, 'members/country_detail.html', {
        'country': country_item,
        'hotels': hotels
    })

# explore cities
def cities (request):
    countries = Country.objects.all()

    return render(request, 'members/cities.html',
       {'countries': countries})


# search cities or else navbar
def search(request):
    query = request.GET.get('q', '')   

    results = []

    if query:
        results = Hotel.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(country__country__icontains=query)
        )

    return render(request, 'members/search_results.html', {
        'hotels': results,
        'query': query
    })

    
# check weather booking is available or not
def checkbook(request):
    destination = request.POST.get('destination')
    guests = request.POST.get('guests')
    message = None
    results = []

    if request.method == "POST" and destination:
        hotels = Hotel.objects.filter(
            Q(country__country__icontains=destination) | Q(city__icontains=destination)
        )
        results = list(hotels)
        if not results:
            message = f"No hotels available in {destination}."

    context = {
        "hotels": results,
        "destination": destination,
        "guests": guests,
        "message": message
    }
    return render(request, "members/checkbook.html", context)

# contact us need help
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully! we will contact u soon")
        return redirect('contact')  
    return render(request, 'members/contact.html') 

#  view btn pages
def hotel_detail(request, id):
    hotel = get_object_or_404(Hotel, id=id)

    comments = HotelComment.objects.filter(hotel=hotel, parent__isnull=True).order_by('-created_at')

    return render(request, "members/hotel_detail.html", {"hotel": hotel, "comments": comments})


# booking details in navbar
@login_required(login_url='/members/?modal=login')
def mybook(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    return render(request, 'members/mybook.html', {'bookings': bookings})


# booking 
@login_required(login_url='/members/index?modal=login')
def book_hotel(request):

    if request.method == "POST":
        hotel_id = request.POST['hotel_id']  
        name = request.POST['name']
        phone = request.POST['phone']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        
        hotel = get_object_or_404(Hotel, id=hotel_id)
        
        Booking.objects.create(
            user=request.user,
            hotel=hotel,
            name=name,
            phone=phone,
            checkin=checkin,
            checkout=checkout
        )

        messages.success(request, "Booking Confirmed Successfully!")
        return redirect('hotel_detail', id=hotel.id)

# cancel booking
@login_required
def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.delete()
    return redirect('mybook')

# sign up modal
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match", extra_tags='signup')
            return redirect(reverse('index') + '?modal=signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered", extra_tags='signup')
            return redirect(reverse('index') + '?modal=signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.last_name = lname     
        user.save()

        messages.success(request, "Account created successfully!", extra_tags='signup')
        return redirect(reverse('index') + '?modal=signup')

    return redirect(reverse('index') + '?modal=signup')

# login modal
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!", extra_tags='login')
            return redirect(reverse('index'))
        else:
            messages.error(request, "Invalid email or password", extra_tags='login')
            return redirect(reverse('index') + '?modal=login')

    return redirect(reverse('index') + '?modal=login')

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')

@login_required(login_url='/members/index?modal=login')
def add_comment(request, id):
    if request.method == "POST":
        hotel = get_object_or_404(Hotel, id=id)
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        parent = None
        if parent_id:
            parent = HotelComment.objects.get(id=parent_id)

        HotelComment.objects.create(
            user=request.user,
            hotel=hotel,
            content=content,
            parent=parent
        )
        messages.success(request, "your message succesfully added")   

    return redirect('hotel_detail', id=id)
