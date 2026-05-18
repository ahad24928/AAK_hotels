from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)  
    city = models.CharField(max_length=100)
    price = models.IntegerField()
    phone = models.CharField(max_length=15, null=True, blank=True) 
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    image = models.ImageField(upload_to='countries/', null=True, blank=True)  # better folder
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    population = models.CharField(max_length=50, blank=True, null=True)
    hotels = models.CharField(max_length=50, blank=True, null=True)
    famous_places = models.CharField(max_length=255, blank=True, null=True)
    climate = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.country}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        

class Booking(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    checkin = models.DateField()
    checkout = models.DateField()

    def __str__(self):
        return self.name

class HotelComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.hotel}"

