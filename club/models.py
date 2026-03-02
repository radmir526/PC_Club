from django.db import models



# Это класс, который описывает наш клуб: его название, адрес, описание
class Club(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# Это класс ддя описания игровых зон в пк клубе
class Zone(models.Model):
    # Константы класса
    STANDARD = 'standard'
    VIP = 'vip'
    BOOTCAMP = 'bootcamp'

    # Это список кортежей для базы данных, каждый кортеж: (значение_в_базе, отображаемое_название)
    ZONE_TYPES = [
        (STANDARD, 'Стандарт'),
        (VIP, 'VIP'),
        (BOOTCAMP, 'Bootcamp')
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=100)
    description = models.TextField()
    zone_type = models.CharField(
        max_length=20,
        choices=ZONE_TYPES, # Разрешаем только эти значения для выбора
        default=STANDARD
    )


    def __str__(self):
        return self.name
    

class ClubImage(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='club_images')
    image = models.ImageField(upload_to='clubs/extra')


class ZoneImage(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='zone_images')
    image = models.ImageField(upload_to='zone/extra')


# Это класс для места, тут есть номер места, ряд, состояние(работает/не работает), и пк, который принадлежит этому месту 
class Seat(models.Model):
    number = models.IntegerField()
    row = models.IntegerField()
    is_active = models.BooleanField(default=True)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name = 'seats')


    class Meta:
        unique_together = ('zone', 'row', 'number') #Объединение пары места и ряда не может повторяться в одном клубе
        ordering = ['zone', 'row', 'number'] # Cортировка по умолчанию
        

    def __str__(self): # Отображение в админке
        return f"{self.zone.name} | Row {self.row} Seat {self.number}"


# Это класс для описания характеристик ПК
class Comp(models.Model):
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.PositiveIntegerField()
    ssd_hdd = models.CharField(max_length=100)
    monitor = models.CharField(max_length=100)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE, related_name='comp')


    def __str__(self):
        return f"CPU {self.cpu} GPU {self.gpu} RAM {self.ram} SSD/HDD {self.ssd_hdd} MONITOR {self.monitor}" 
    

class Tariff(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='tariffs')
    name = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    duration_hours = models.IntegerField()

    
    def __str__(self):
        return f"{self.name} - {self.price_per_hour}₽/час"