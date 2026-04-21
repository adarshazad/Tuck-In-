import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from accounts.models import User

admin_username = 'admin'
admin_password = 'admin123'
admin_email = 'admin@helpdesk.com'

if not User.objects.filter(username=admin_username).exists():
    print(f"Creating superuser {admin_username}...")
    admin = User.objects.create_superuser(admin_username, admin_email, admin_password)
    admin.role = 'admin'
    admin.first_name = 'Admin'
    admin.last_name = 'User'
    admin.save()
    print("Admin created successfully.")
else:
    print(f"Superuser {admin_username} already exists. Skipping creation.")

# Also ensure agent1 exists
agent_username = 'agent1'
agent_password = 'agent123'
if not User.objects.filter(username=agent_username).exists():
    print(f"Creating agent {agent_username}...")
    agent = User.objects.create_user(agent_username, 'agent@helpdesk.com', agent_password)
    agent.role = 'agent'
    agent.first_name = 'Rahul'
    agent.last_name = 'Sharma'
    agent.save()
    print("Agent created successfully.")
else:
    print(f"Agent {agent_username} already exists. Skipping creation.")
