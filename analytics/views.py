from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from tickets.models import Ticket
from accounts.models import User
import json
from datetime import datetime, timedelta

@login_required
def analytics_dashboard(request):
    if request.user.role not in ['admin', 'agent']:
        from django.shortcuts import redirect
        return redirect('dashboard')

    last_30 = datetime.now() - timedelta(days=30)

    # Ticket trends by day
    ticket_trend = (
        Ticket.objects.filter(created_at__gte=last_30)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    trend_labels = [str(t['date']) for t in ticket_trend]
    trend_data = [t['count'] for t in ticket_trend]

    # Status distribution
    status_data = Ticket.objects.values('status').annotate(count=Count('id'))
    status_labels = [s['status'].title() for s in status_data]
    status_counts = [s['count'] for s in status_data]

    # Agent performance
    agent_perf = (
        Ticket.objects.filter(assigned_to__isnull=False)
        .values('assigned_to__username')
        .annotate(total=Count('id'), resolved=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(status='resolved')))
        .order_by('-total')[:5]
    )

    context = {
        'trend_labels': json.dumps(trend_labels),
        'trend_data': json.dumps(trend_data),
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
        'agent_perf': agent_perf,
        'total_tickets': Ticket.objects.count(),
        'open_tickets': Ticket.objects.filter(status='open').count(),
        'resolved_tickets': Ticket.objects.filter(status='resolved').count(),
    }
    return render(request, 'analytics/dashboard.html', context)
