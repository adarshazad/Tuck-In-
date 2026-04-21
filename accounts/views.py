from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User

def login_view(request):
    # If already logged in and this is a GET request, redirect to dashboard
    if request.user.is_authenticated and request.method == 'GET':
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If someone is already logged in, log them out first before switching
        if request.user.is_authenticated:
            logout(request)

        # Auto-provisioning: Re-inject hardcoded staff users if Render wiped the DB
        HARDCODED_USERS = {
            'admin':  ('admin123', 'superuser', 'admin', 'Admin',  'User',   'admin@helpdesk.com'),
            'agent1': ('agent123', 'user',      'agent', 'Rahul',  'Sharma', 'agent1@helpdesk.com'),
            'agent2': ('agent456', 'user',      'agent', 'Priya',  'Verma',  'agent2@helpdesk.com'),
            'agent3': ('agent789', 'user',      'agent', 'Amit',   'Khanna', 'agent3@helpdesk.com'),
        }
        if username in HARDCODED_USERS and password == HARDCODED_USERS[username][0]:
            pw, utype, role, first, last, email = HARDCODED_USERS[username]
            if not User.objects.filter(username=username).exists():
                if utype == 'superuser':
                    u = User.objects.create_superuser(username, email, pw)
                else:
                    u = User.objects.create_user(username, email, pw)
                u.role, u.first_name, u.last_name = role, first, last
                u.save()
            user_obj = User.objects.get(username=username)
            login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')

        # Normal login for regular registered users
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password. Please try again.')

            
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
