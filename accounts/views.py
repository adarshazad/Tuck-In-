from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User

HARDCODED_USERS = {
    'admin':  {'password': 'admin123', 'type': 'superuser', 'role': 'admin',  'first': 'Admin',  'last': 'User',   'email': 'admin@helpdesk.com'},
    'agent1': {'password': 'agent123', 'type': 'user',      'role': 'agent',  'first': 'Rahul',  'last': 'Sharma', 'email': 'agent1@helpdesk.com'},
    'agent2': {'password': 'agent456', 'type': 'user',      'role': 'agent',  'first': 'Priya',  'last': 'Verma',  'email': 'agent2@helpdesk.com'},
    'agent3': {'password': 'agent789', 'type': 'user',      'role': 'agent',  'first': 'Amit',   'last': 'Khanna', 'email': 'agent3@helpdesk.com'},
}

def _ensure_hardcoded_user(username):
    """Create the hardcoded user if missing, return the user object."""
    info = HARDCODED_USERS[username]
    if not User.objects.filter(username=username).exists():
        if info['type'] == 'superuser':
            u = User.objects.create_superuser(username, info['email'], info['password'])
        else:
            u = User.objects.create_user(username, info['email'], info['password'])
        u.role       = info['role']
        u.first_name = info['first']
        u.last_name  = info['last']
        u.is_active  = True
        u.save()
    else:
        # Ensure password is always correct even if it drifted
        u = User.objects.get(username=username)
        if not u.check_password(info['password']):
            u.set_password(info['password'])
        u.role = info['role']
        u.is_active = True
        u.save()
    return User.objects.get(username=username)

def login_view(request):
    # GET: if already logged in, go to dashboard
    if request.user.is_authenticated and request.method == 'GET':
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Always clear any existing session before a new login attempt
        if request.user.is_authenticated:
            logout(request)

        # ── HARDCODED STAFF USERS ─────────────────────────────────────────
        # These bypass form validation entirely so Render DB wipes never matter
        if username in HARDCODED_USERS:
            if password == HARDCODED_USERS[username]['password']:
                user_obj = _ensure_hardcoded_user(username)
                login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard')
            else:
                # Correct username but wrong password
                messages.error(request, 'Incorrect password for this account.')
                return render(request, 'accounts/login.html', {'form': LoginForm(request)})

        # ── REGULAR REGISTERED USERS ──────────────────────────────────────
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password. Please try again.')
            return render(request, 'accounts/login.html', {'form': form})

    # GET request – show blank login form
    return render(request, 'accounts/login.html', {'form': LoginForm(request)})


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
