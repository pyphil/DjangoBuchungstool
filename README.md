# DjangoBuchungstool

### Virtual Environment
```
python3 -m venv .venv

.venv/Scripts/Activate.ps1 (Windows)

source .venv/bin/activate (Linux)
```

### Install Django in venv
```
python3 -m pip install django
```

### Migrate migrations to new db
```
python3 manage.py migrate
```

### Create superuser for /admin/
```
python3 manage.py createsuperuser
```
