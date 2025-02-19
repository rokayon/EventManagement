from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib import messages
from datetime import date
from .models import Event, Participant, Category
from .forms import EventForm, CategoryForm, ParticipantForm

# ORGANIZER DASHBOARD 

def organizer_dashboard(request):
    """Dashboard with event statistics and today's events"""
    stats = {
        'total_participants': Participant.objects.count(),
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

def event_create(request):
    """Create a new event"""
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

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

def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

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

def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})

# PARTICIPANT VIEWS 

def participant_list(request):
    """List all participants with their registered events"""
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'participants/participant_list.html', {'participants': participants})

def participant_create(request):
    """Create a new participant and assign events"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.save()
            form.save_m2m()  
            messages.success(request, 'Participant created successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participants/participant_form.html', {'form': form})

def participant_update(request, pk):
    """Update a participant's details and event registrations"""
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant updated successfully!')
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participants/participant_form.html', {'form': form})

def participant_delete(request, pk):
    """Delete a participant"""
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'Participant deleted successfully!')
        return redirect('participant_list')
    return render(request, 'participants/participant_confirm_delete.html', {'participant': participant})
