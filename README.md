# DjangoBuchungstool

### Virtual Environment
```
python3 -m venv .venv

.venv/Scripts/activate (Windows)

source .venv/bin/activate (Linux)
```

### Install Django in venv
```
python -m pip install django
```

### Migrate migrations to new db
```
python manage.py migrate
```

### Create superuser for /admin/
```
python manage.py createsuperuser
```

### Run development server
```
python manage.py runserver
```
