from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from events.views import organizer_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', organizer_dashboard, name='home'),  
    path('events/', include('events.urls')),
    path('participants/', include('events.urls')),  
    path('categories/', include('events.urls')),   
]+ debug_toolbar_urls()