from django.db import models
from django.contrib.auth.models import User

class Sport(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # Custom ID like 'badminton'
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

from datetime import date

class Court(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='courts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sport.name} - {self.name}"

    def get_status(self, time_slot, check_date=None):
        check_date = check_date or date.today()
        booking = Booking.objects.filter(court=self, time_slot=time_slot, date=check_date).first()
        if booking:
            return booking.status
        return BookingStatus.AVAILABLE


class TimeSlot(models.Model):
    hour = models.IntegerField()  # 24-hour format
    @property
    def formatted_slot(self):
        # Format like "9:00 AM", "2:30 PM", etc.
        hour_12 = self.hour % 12
        if hour_12 == 0:
            hour_12 = 12
        am_pm = "AM" if self.hour < 12 else "PM"
        return f"{hour_12}"
    
    def __str__(self):
        return self.formatted_slot

class BookingStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    BOOKED = 'booked', 'Booked'
    MAINTENANCE = 'maintenance', 'Under Maintenance'
    RESERVED = 'reserved', 'Reserved'

class Booking(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.BOOKED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('court', 'time_slot', 'date')
    
    def __str__(self):
        return f"{self.court} - {self.date} - {self.time_slot}"