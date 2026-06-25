#!/bin/sh
python manage.py migrate --run-syncdb
python manage.py shell <<'PY'
from django.contrib.auth.models import User
user, _ = User.objects.get_or_create(username="root")
user.email = "root@example.com"
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password("root")
user.save()
print("root admin ready")
PY
python manage.py runserver 0.0.0.0:8000
