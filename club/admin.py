from django.contrib import admin
from .models import Club, Seat, Zone, Comp, ClubImage, ZoneImage, Tariff


class ClubImageInline(admin.TabularInline):
    model = ClubImage
    extra = 1


class ZoneImageInline(admin.TabularInline):
    model = ZoneImage
    extra = 1


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'address']
    list_filter = ['address']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClubImageInline]


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['club', 'name', 'zone_type']
    list_filter = ['club', 'zone_type']
    search_fields = ['club__name', 'description']
    inlines = [ZoneImageInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['zone', 'row', 'number', 'is_active']
    list_filter = ['zone', 'is_active']
    search_fields = ['zone__name']



@admin.register(Comp)
class CompAdmin(admin.ModelAdmin):
    list_display = [ 'get_zone', 'get_row', 'get_number', 
                    'cpu','gpu', 'ram', 'ssd_hdd', 'monitor']
    
    list_filter = ['seat__zone', 'cpu','gpu', 'ram', 
                   'ssd_hdd', 'monitor']
    search_fields = ['seat__number', 'seat__zone__name', 'cpu', 'gpu']

    def get_zone(self, obj):
        return obj.seat.zone
    get_zone.short_description = 'Zone'


    def get_row(self, obj):
        return obj.seat.row
    get_row.short_description = 'Row'


    def get_number(self, obj):
        return obj.seat.number
    get_number.short_description = 'Seat Number'


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['zone', 'name', 'price_per_hour', 'duration_hours']
