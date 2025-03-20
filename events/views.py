from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib import messages
from datetime import date
from .models import Event,Category
from .forms import EventForm, CategoryForm
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.contrib.auth import get_user_model
from users.views import is_admin
from django.contrib.auth.models import User

# ORGANIZER DASHBOARD 

def get_user_with_groups(user_id):
    return get_user_model().objects.prefetch_related('groups').get(id=user_id)
def is_Organizer(user):
    return user.groups.filter(name__iexact='Organizer').exists()
def is_Participant(user):
    return user.groups.filter(name__iexact='Participant').exists()
def is_Organizer_or_Admin(user):
    return is_admin or user.groups.filter(name__iexact='Organizer').exists()

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.participants.all():
        event.participants.remove(user)
        messages.success(request, f'You have un-RSVPed from {event.name}.')
    else:
        event.participants.add(user)
        messages.success(request, f'You have RSVP’d for {event.name}.')

    return redirect('dashboard') 

@login_required
def participant_dashboard(request):
    """Display events the user has RSVP’d to."""
    rsvp_events = request.user.rsvp_events.all()
    return render(request, "dashboard/users_dashboard.html", {"rsvp_events": rsvp_events})
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def organizer_dashboard(request):
    """Dashboard with event statistics and today's events"""
    stats = {
        'total_participants': Event.participants.through.objects.count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=date.today()).count(),
        'past_events': Event.objects.filter(date__lt=date.today()).count(),
    }
    todays_events = Event.objects.filter(date=date.today()).select_related('category')
    return render(request, 'dashboard/organizer_dashboard.html', {'stats': stats, 'todays_events': todays_events})

# EVENT VIEWS 

def event_list(request):
    """List all events with optimized queries"""
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    """View event details"""
    event = get_object_or_404(Event.objects.prefetch_related('participants'), pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def event_create(request):
    """Create a new event"""
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def event_update(request, pk):
    """Update an existing event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def event_delete(request, pk):
    """Delete an event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def search_events(request):
    """Search events by name or location"""
    query = request.GET.get('q', '')
    events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query)) if query else Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events, 'query': query})

#  CATEGORY VIEWS 
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def category_update(request, pk):
    """Update an existing category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})
@user_passes_test(is_Organizer_or_Admin, login_url='no-permission')
def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})


