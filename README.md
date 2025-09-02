
# AgTech ERP Platform Backend

Its a cooperative management **web application system** built with **Django** that allows an **Admin** to manage farmers and their crops, while **Farmers** can manage their own profiles and crops.

## 📜 License

This project is licensed under a **Proprietary License**.  

## Getting Started

Follow these steps to clone the repository and run the server on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/marywam/Agri-Records-Backend.git

cd Agri-Records-Backend

```

### 2. Set up the virtual environment

```bash
python3 -m venv <your-env-name>
source <your-env-name>/bin/activate

# 👉 **Example**
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Upgrade pip (recommended)

```bash
python -m pip install --upgrade pip

```

### 4. Install Django

```bash
pip install django

```

### 5. Create the Django project

```bash
python -m django startproject agritech

cd agritech

```

### 6. Create a Django app

```bash
django-admin startapp agriTechApp

```

### 7. Create a requirements file

```bash
cd ..
touch requirements.txt

```

### 8. Install essential packages

```bash
pip install djangorestframework
pip install django-cors-headers
pip install python-dotenv

```

### 9. Update Django settings

```python
# settings.py

INSTALLED_APPS = [
    # other default apps...
    'rest_framework',
    'corsheaders',
    'agriTechApp',
]

MIDDLEWARE = [
    # other default middleware...
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

```

### 10. Freeze dependencies and push to Git

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add REST framework and dependencies"
git push

```

### 11. Run initial migrations and start the server

```bash
cd agritech
python manage.py migrate
python manage.py runserver

```

## ✅ You're Live

Visit <http://127.0.0.1:8000> to access the development server.





