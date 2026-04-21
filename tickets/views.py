from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, TicketComment
from .forms import TicketForm, TicketUpdateForm, CommentForm

@login_required
def ticket_list(request):
    user = request.user
    status_filter = request.GET.get('status', '')

    if user.role == 'admin':
        tickets = Ticket.objects.all()
    elif user.role == 'agent':
        tickets = Ticket.objects.filter(assigned_to=user)
    else:
        tickets = Ticket.objects.filter(created_by=user)

    if status_filter:
        tickets = tickets.filter(status=status_filter)

    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets,
        'status_filter': status_filter,
    })

@login_required
def ticket_create(request):
    if request.user.role == 'admin':
        messages.error(request, "Admins cannot create tickets. They can only resolve them.")
        return redirect('dashboard')
    
    form = TicketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.created_by = request.user
        ticket.save()
        messages.success(request, 'Ticket created successfully!')
        return redirect('tickets:detail', pk=ticket.pk)
    return render(request, 'tickets/ticket_form.html', {'form': form, 'title': 'Create Ticket'})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.ticket = ticket
        comment.author = request.user
        comment.save()
        messages.success(request, 'Comment added!')
        return redirect('tickets:detail', pk=pk)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'comment_form': comment_form})

@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user.role not in ['admin', 'agent'] and ticket.created_by != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('tickets:list')
    form = TicketUpdateForm(request.POST or None, instance=ticket) if request.user.role in ['admin', 'agent'] else TicketForm(request.POST or None, instance=ticket)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ticket updated!')
        return redirect('tickets:detail', pk=pk)
    return render(request, 'tickets/ticket_form.html', {'form': form, 'ticket': ticket, 'title': 'Update Ticket'})

@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user.role == 'admin' or ticket.created_by == request.user:
        ticket.delete()
        messages.success(request, 'Ticket deleted.')
    return redirect('tickets:list')
