from django.db import models
from club.models import Club, Zone, Seat, Tariff
from accounts.models import CustomUser


class BookingTime(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_users')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='bookings_tariffs')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings_seats')
    total_price = models.DecimalField(max_digits=6, decimal_places=2)


    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Ожидает'),
        (ACTIVE, 'Активна'),
        (COMPLETED, 'Завершена'),
        (CANCELLED, 'Отменена')
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.user} - {self.seat} - {self.status}"
