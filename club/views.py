from .models import Comp, Zone, Seat, Club, Tariff
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Prefetch
from django.template.response import TemplateResponse

# При заходе на страницу, сразу выводятся все клубы
class IndexView(ListView):
    model = Club # говорим джанго с какой станицей работаем
    template_name = 'main/index.html' # какой шаблон использовать
    context_object_name = 'clubs' # под каким именем список клубов будет доступен в шаблоне

    # этот метод срабатывает когда браузер делает GET запрос
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs) # тут мы берем все из базы данных. Делаем то, что делает страндартный DetailView или ListView
        if request.headers.get('HX-Request'): # Если запрос от HTMX
            return TemplateResponse(request, 'main/partials/index.html', response.context_data) # То возвращаем только кусок HTML без шапки и футера. Response.context_data - это данные, которые уже подготовил super()
        return response # Если запрос обычный, то возвращаем полную страницу


class ClubDetailView(DetailView):
    model = Club
    template_name = 'main/club_detail.html'
    context_object_name = 'club'
    slug_field = 'slug' # говорим Django что в модели Club есть поле slug, ищи по нему
    slug_url_kwarg = 'slug' # говорим Django что в URL это называется slug

    # Когда Django находит клуб в базе, он делает запрос. 
    # Но нам нужны не только данные клуба, но и его фотографии, зоны, фотографии зон, тарифы. 
    # Без `prefetch_related` Django делал бы кучу отдельных запросов к базе — это медленно. 
    # А `prefetch_related` говорит: "подтяни всё это одним махом".
    def get_queryset(self):
        return Club.objects.prefetch_related(
            'club_images',
            Prefetch(
                'zones',
                queryset=Zone.objects.prefetch_related(
                    'zone_images',
                    'tariffs'
                )
            )
        )
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/partials/club_detail.html', response.context_data)
        return response
    
# views для выбора места. Используем модель zone в ней уже есть ее описание, 
# а так же информация из класса Seats о местах 
class SelectSeatView(DetailView):
    model = Zone
    template_name = 'main/select_seat.html'
    context_object_name = 'zone'
    
    # Тут мы получаем сразу все данные из класса Seat
    def get_queryset(self):
        return Zone.objects.prefetch_related('seats', 'zone_images', 'tariffs')
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/partials/select_seat.html', response.context_data)
        return response