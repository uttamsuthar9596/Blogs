# 📝 Django Blog Application with MySQL

This is a full-featured **Blog Application** built using **Django**, **Django REST Framework**, **MySQL**, and **JWT Authentication**. It allows users to register, log in, create and manage their own blog posts, view others’ posts, and interact with the content via a dynamic frontend.

---

## ⚙️ Project Setup (Start Here)

Follow these steps to set up the project on your local system:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/blog-app-django.git
cd blog-app-django
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate
```

### 3️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure MySQL Database

Open `blog_project/settings.py` and update your database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

> Make sure your MySQL server is running and the database exists.

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Start the Development Server

```bash
python manage.py runserver
```

---

## 🌐 Project URLs

### 🖥 Web URLs

| URL | Description |
|-----|-------------|
| `/` | Shows the homepage with a list of all blog posts |
| `/posts/<post_id>/` | Opens a full view of a specific blog post |
| `/register/` | Page where new users can sign up |
| `/login/` | Page where existing users can log in |
| `/logout/` | Logs out the currently logged-in user |
| `/create/` | Allows a logged-in user to create a new blog post |
| `/posts/<post_id>/edit/` | Lets the original author edit their blog post |

---

### 🔗 API URLs

| URL | Description |
|-----|-------------|
| `/api/posts/` | Get a list of all blog posts or add a new one (requires login) |
| `/api/posts/<id>/` | Get, update, or delete one specific blog post by its ID |
| `/api/auth/` | Used to log in and get a JWT token for API use |
| `/api/auth/refresh/` | Used to refresh the JWT access token when it expires |
| `/api/register/` | Allows new users to sign up using the API |

---



## 📢 Notes

- Don't forget to replace placeholders like `your-username`, `your_db_name`, etc.
