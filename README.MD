# Join Backend – Django Project

This is the backend for my Join project, built using Django and Django REST Framework.

## 🚀 Features

- User registration and login with token-based authentication
- Contact management (Create, Read, Update, Delete)
- RESTful API with Django REST Framework (DRF)

## 🛠 Installation

1. Clone the repository:
    git clone https://github.com/cyborg-s/JoinBackend.git
    cd JoinBackend

2. Create and activate a virtual environment:
    python -m venv env
    env\Scripts\activate (Windows)

3. Install dependencies:
    pip install -r requirements.txt

4. Apply database migrations:
    python manage.py migrate

5. Start the development server:
    python manage.py runserver



Projekt struktur:

BACKEND/
│
├── manage.py
├── join_backend/       # Django project settings
├── join_BE/            # Application logic and views
└── README.md





Contributors
This project was developed and maintained by Sascha Nyssen.
Contributions, suggestions, and improvements are always welcome. Feel free to open an issue or submit a pull request.


License
This project is licensed under the MIT License.
You are free to use, modify, and distribute this software, provided that the original copyright notice and permission notice are included 
in all copies or substantial portions of the Software.