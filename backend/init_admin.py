import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

User = get_user_model()
username = 'admin'
password = 'admin'

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, password=password, email='admin@example.com', is_admin=True)
    print("Superuser created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
