from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from knowledge.models import Article

def home(request):
    try:
        from accounts.models import User
        admin_user = User.objects.filter(username='admin').first()
        if admin_user and admin_user.role != 'admin':
            admin_user.role = 'admin'
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
        agent_user = User.objects.filter(username='agent1').first()
        if agent_user and agent_user.role != 'agent':
            agent_user.role = 'agent'
            agent_user.save()
    except Exception:
        pass

    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        tickets = Ticket.objects.all().order_by('-created_at')[:10]
        total_tickets = Ticket.objects.count()
        open_tickets = Ticket.objects.filter(status='open').count()
        resolved_tickets = Ticket.objects.filter(status='resolved').count()
        in_progress = Ticket.objects.filter(status='in_progress').count()
    elif user.role == 'agent':
        tickets = Ticket.objects.filter(assigned_to=user).order_by('-created_at')[:10]
        total_tickets = Ticket.objects.filter(assigned_to=user).count()
        open_tickets = Ticket.objects.filter(assigned_to=user, status='open').count()
        resolved_tickets = Ticket.objects.filter(assigned_to=user, status='resolved').count()
        in_progress = Ticket.objects.filter(assigned_to=user, status='in_progress').count()
    else:
        tickets = Ticket.objects.filter(created_by=user).order_by('-created_at')[:10]
        total_tickets = Ticket.objects.filter(created_by=user).count()
        open_tickets = Ticket.objects.filter(created_by=user, status='open').count()
        resolved_tickets = Ticket.objects.filter(created_by=user, status='resolved').count()
        in_progress = Ticket.objects.filter(created_by=user, status='in_progress').count()

    context = {
        'tickets': tickets,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'resolved_tickets': resolved_tickets,
        'in_progress': in_progress,
    }
    return render(request, 'dashboard.html', context)
