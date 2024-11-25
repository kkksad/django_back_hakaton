from django.urls import path
from .views import CreateEventView, EditEventView, DeleteEventView, JoinEventView, UnjoinEventView, ListEventsView

urlpatterns = [
    path('create_event/', CreateEventView.as_view(), name='create_event'),
    path('edit_event/<int:pk>/', EditEventView.as_view(), name='edit_event'),
    path('delete_event/<int:pk>/', DeleteEventView.as_view(), name='delete_event'),
    path('join_event/', JoinEventView.as_view(), name='join_event'),
    path('unjoin_event/', UnjoinEventView.as_view(), name='unjoin_event'),
    path('list_events/', ListEventsView.as_view(), name='list_events'),
]
