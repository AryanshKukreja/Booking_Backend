from django.contrib import admin
from .models import Sport, Court, TimeSlot, Booking

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport')
    list_filter = ('sport',)
    search_fields = ('name',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('formatted_slot', 'hour')
    ordering = ('hour',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('court', 'time_slot', 'date', 'status', 'user', 'updated_at')
    list_filter = ('status', 'date', 'court__sport')
    search_fields = ('court__name', 'user__username')
    date_hierarchy = 'date'