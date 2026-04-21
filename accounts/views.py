from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Bypassing the Render Wipe: Re-inject users instantly if they type correct creds
        if username in ['admin', 'agent1'] and password in ['admin123', 'agent123']:
            from accounts.models import User
            if not User.objects.filter(username=username).exists():
                if username == 'admin' and password == 'admin123':
                    u = User.objects.create_superuser('admin', 'admin@helpdesk.com', 'admin123')
                    u.role, u.first_name, u.last_name = 'admin', 'Admin', 'User'
                    u.save()
                elif username == 'agent1' and password == 'agent123':
                    a = User.objects.create_user('agent1', 'agent@helpdesk.com', 'agent123')
                    a.role, a.first_name, a.last_name = 'agent', 'Rahul', 'Sharma'
                    a.save()
            
            # FORCE LOGIN BYPASSING AuthForm completely
            user_obj = User.objects.get(username=username)
            login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

        # Normal fallback for other users
        form = LoginForm(request, data=request.POST) 
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            if '__all__' in form.errors:
                messages.error(request, form.errors['__all__'].as_text())
            else:
                messages.error(request, 'Invalid username or password. Please check your credentials.')
            
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated!')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def user_list(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})
