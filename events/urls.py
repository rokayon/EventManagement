from django.urls import path
from .views import (
    organizer_dashboard, event_list, event_detail, event_create, event_update, event_delete,
    search_events, category_list, category_create, category_update, category_delete,
    participant_list, participant_create, participant_update, participant_delete
)

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('create/', event_create, name='event_create'),
    path('<int:pk>/update/', event_update, name='event_update'),
    path('<int:pk>/delete/', event_delete, name='event_delete'),
    path('search/', search_events, name='search_events'),
    path('dashboard/', organizer_dashboard, name='organizer_dashboard'),

    # Category URLs
    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/<int:pk>/update/', category_update, name='category_update'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),

    # Participant URLs
    path('participants/', participant_list, name='participant_list'),
    path('participants/create/', participant_create, name='participant_create'),
    path('participants/<int:pk>/update/', participant_update, name='participant_update'),
    path('participants/<int:pk>/delete/', participant_delete, name='participant_delete'),
]


