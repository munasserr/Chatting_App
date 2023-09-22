from .views import index,rooms,loginview,logout
from django.urls import path

urlpatterns = [
    path('login/', loginview ,name='login'),
    path('logout/', logout ,name='logout'),
    path('lobby/', index ,name='chat'),
    path("<str:room_id>/", rooms, name="room"),
]