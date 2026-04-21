from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from tickets.models import Ticket
from knowledge.models import Article
from accounts.models import User

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    user = request.user
    base_queryset = Ticket.objects.none()  # Start with an empty queryset

    if user.role == 'admin':
        base_queryset = Ticket.objects.all()
    elif user.role == 'agent':
        base_queryset = Ticket.objects.filter(assigned_to=user)
    else:
        base_queryset = Ticket.objects.filter(created_by=user)

    context = {
        'tickets': base_queryset.order_by('-created_at')[:10],
        'total_tickets': base_queryset.count(),
        'open_tickets': base_queryset.filter(status='open').count(),
        'resolved_tickets': base_queryset.filter(status='resolved').count(),
        'in_progress': base_queryset.filter(status='in_progress').count(),
    }
    return render(request, 'dashboard.html', context)
