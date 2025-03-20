from django.shortcuts import render,redirect
from events.views  import is_Organizer
from users.views import is_admin
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'home.html')
def no_permission(request):
    return render(request, 'no_parmission.html')
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Dashboard views"""
    user = request.user
    
    # Check permissions in order of priority
    if user.is_superuser or is_admin(user):
        return redirect('admin-dashboard')
    elif is_Organizer(user):
        return redirect('organizer_dashboard')
    else:
        return redirect('participant_dashboard')
   