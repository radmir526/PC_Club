from django.urls import path
from . import views

app_name = 'club'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('clubs/<slug:slug>', views.ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<slug:slug>/zone/<int:pk>', views.SelectSeatView.as_view(), name = 'select_seat')
]