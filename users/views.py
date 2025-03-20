from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Prefetch


def is_admin(user):
    """
    Check if the user belongs to the 'superadmin' group
    """
    user = get_user_model().objects.get(id=user.id)  # Reload user data
    return user.groups.filter(name__iexact='admin').exists()


def user_sign_up(request):
    if request.method == 'GET':
        registration_form = CustomRegistrationForm()
    if request.method == 'POST':
        registration_form = CustomRegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data.get('password1'))
            new_user.is_active = False
            new_user.save()
            messages.success(request, "Confirmation email has been sent. Please check your inbox.")
            return redirect('sign-in')
        else:
            messages.error(request, "Form submission failed, please try again.")
            print("Password mismatch or other form errors")
    return render(request, 'registration/register.html', {'form': registration_form})


def user_sign_in(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            authenticated_user = login_form.get_user()
            login(request, authenticated_user)
            return redirect('dashboard')
    return render(request, 'registration/login.html', {'form': login_form})


@login_required
def user_sign_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('sign-in')


def activate_user_account(request, user_id, token):
    try:
        user_to_activate = User.objects.get(id=user_id)
        if default_token_generator.check_token(user_to_activate, token):
            user_to_activate.is_active = True
            user_to_activate.save()
            return redirect('sign-in')
        else:
            user_to_activate.is_active = False
            return HttpResponse('Invalid token or user ID')
    except User.DoesNotExist:
        return HttpResponse('User not found')


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    all_users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='user_groups')
    ).all()

    for user in all_users:
        if user.user_groups:
            user.role_name = user.user_groups[0].name
        else:
            user.role_name = 'No Group Assigned'

    return render(request, 'admin/admin_dashboard.html', {'users': all_users})


@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
  user=User.objects.get(id=user_id)
  form=AssignRoleForm()
  if request.method == 'POST':
    form=AssignRoleForm(request.POST)
    if form.is_valid():
       role=form.cleaned_data.get('role')
       user.groups.clear() #remove the old roles
       user.groups.add(role)#add the new roles
       messages.success(request,f"User {user.username} has been assigned to {role.name} Role")
       return redirect('admin-dashboard')
  return render(request,'admin/assign_role.html',{'form':form})   

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()  # Save the group
            group.permissions.set(form.cleaned_data['permissions'])  # Set the permissions
            messages.success(request, f'Group {group.name} has been created successfully!')
            return redirect('create-group')
    else:
        form = CreateGroupForm()
    
    return render(request, 'admin/create_group.html', {'form': form})
@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
  groups=Group.objects.prefetch_related('permissions').all()
  return render(request,'admin/group_list.html',{'groups':groups})
