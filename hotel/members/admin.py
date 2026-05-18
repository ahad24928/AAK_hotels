from django.contrib import admin
from .models import Hotel, Booking, Contact, HotelComment, Country

admin.site.register(Booking)
admin.site.register(Hotel)
admin.site.register(Contact)
admin.site.register(HotelComment)
admin.site.register(Country)
