import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from accounts.models import User
from tickets.models import Ticket, TicketComment
from knowledge.models import Category, Article

print("Seeding demo data...")

# Create users
admin = User.objects.create_superuser('admin', 'admin@helpdesk.com', 'admin123')
admin.role = 'admin'
admin.first_name = 'Admin'
admin.last_name = 'User'
admin.save()

agent = User.objects.create_user('agent1', 'agent@helpdesk.com', 'agent123')
agent.role = 'agent'
agent.first_name = 'Rahul'
agent.last_name = 'Sharma'
agent.save()

agent2 = User.objects.create_user('agent2', 'agent2@helpdesk.com', 'agent123')
agent2.role = 'agent'
agent2.first_name = 'Priya'
agent2.last_name = 'Singh'
agent2.save()

agent3 = User.objects.create_user('agent3', 'agent3@helpdesk.com', 'agent123')
agent3.role = 'agent'
agent3.first_name = 'Amit'
agent3.last_name = 'Kumar'
agent3.save()

user1 = User.objects.create_user('john_doe', 'john@example.com', 'user123')
user1.role = 'user'
user1.first_name = 'John'
user1.last_name = 'Doe'
user1.save()

print("Users created: admin / agent1 / agent2 / agent3 / john_doe")
print("Passwords:     admin123 / agent123 / user123")

# Knowledge categories
cat1 = Category.objects.create(name='Getting Started', description='Basic setup and usage guides')
cat2 = Category.objects.create(name='Account and Billing', description='Account management topics')
cat3 = Category.objects.create(name='Troubleshooting', description='Common issues and fixes')

# Articles
Article.objects.create(
    title='How to create a support ticket',
    content='To create a support ticket:\n\n1. Log in to your account.\n2. Click "New Ticket" in the top navigation bar.\n3. Fill in the title and describe your issue in detail.\n4. Click "Submit Ticket".\n\nOnce submitted, our support team will be notified and respond within 24 hours.',
    category=cat1, author=admin, is_published=True
)
Article.objects.create(
    title='How to reset your password',
    content='If you have forgotten your password:\n\n1. Go to the login page.\n2. Click "Forgot Password".\n3. Enter your registered email address.\n4. Check your email inbox for the reset link.\n5. Click the link and set a new password.\n\nIf you do not receive the email within 5 minutes, please check your spam or junk folder.',
    category=cat2, author=agent, is_published=True
)
Article.objects.create(
    title='Why is my ticket showing as "Unassigned"?',
    content='Tickets may appear as "Unassigned" for the following reasons:\n\n- The ticket was just submitted and is awaiting assignment by an admin.\n- No agents are currently available for that category.\n\nOur admin team assigns tickets based on agent availability.\n\nIf your ticket remains unassigned for more than 24 hours, please add a comment to it and our team will follow up.',
    category=cat3, author=admin, is_published=True
)

print("Knowledge base articles created.")

# Tickets
t1 = Ticket.objects.create(
    title='Cannot log in to my account',
    description='I am unable to log in despite entering the correct credentials. The error message says "Invalid username or password" but I am certain the details are correct. I tried resetting the password but the reset email is not arriving in my inbox.',
    status='open',
    created_by=user1, assigned_to=agent
)
t2 = Ticket.objects.create(
    title='Dashboard not loading properly',
    description='The dashboard shows a blank white screen immediately after I log in. I have tried clearing the browser cache and using a different browser, but the issue persists across all of them.',
    status='in_progress',
    created_by=user1, assigned_to=agent
)
t3 = Ticket.objects.create(
    title='How do I export my ticket history?',
    description='I need to export all my past tickets to a CSV or Excel file for internal record-keeping purposes. I could not find an export option in the dashboard. Could you please guide me?',
    status='resolved',
    created_by=user1, assigned_to=agent
)

t4 = Ticket.objects.create(
    title='Email notifications are delayed',
    description='I am receiving email notifications 2 hours after the actual event. Please fix this.',
    status='open',
    created_by=user1, assigned_to=agent2
)

t5 = Ticket.objects.create(
    title='Unable to update billing information',
    description='The credit card update page throws a 500 internal server error.',
    status='in_progress',
    created_by=user1, assigned_to=agent3
)

TicketComment.objects.create(
    ticket=t1, author=agent,
    content='Hi John, thank you for reaching out. I have escalated this to the technical team and we will resolve this as soon as possible.'
)
TicketComment.objects.create(
    ticket=t2, author=agent,
    content='Could you please share your browser name and version? Also, do you see any error messages in the browser developer console?'
)
TicketComment.objects.create(
    ticket=t3, author=agent,
    content='The ticket export feature is currently on our development roadmap. For now, you can use the browser print function (Ctrl+P) to save the ticket list as a PDF. Marking this ticket as resolved.'
)
TicketComment.objects.create(
    ticket=t3, author=user1,
    content='Thank you for the quick response! The PDF option works for now.'
)
TicketComment.objects.create(
    ticket=t5, author=agent3,
    content='I am checking the server logs to identify the root cause of this 500 error.'
)

print("Demo tickets and comments created.")
print("")
print("Setup complete. Run the server and visit http://127.0.0.1:8000")
print("Login with: admin / admin123")
