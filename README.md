Here's the beautified README file for your project:

```markdown
### Django REST Framework - API for N2Mobil

This is a simple API for user tracking system, developed using Django REST Framework.

## Getting Started

# Clone the Repository

git clone https://github.com/yunusemre482/n2mobil_backend.git
```

## Running the Project

You can run the project using Docker Compose or a virtual environment.

### Running with Docker Compose

1. **Build and start the containers:**
    ```bash
    docker-compose up -d --build
    ```

2. **Run the migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

3. **Access the PostgreSQL database:**
    Visit [http://localhost:8080](http://localhost:8080).

### Running with Virtual Environment

1. **Navigate to the project directory:**
    ```bash
    cd n2mobil_backend
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the server:**
    ```bash
    python manage.py runserver
    ```

8. **Access the admin panel:**
    Visit [http://localhost:8000/admin/](http://localhost:8000/admin/) and log in with the superuser credentials created in step 6.

## API Endpoints

- **User Endpoints:**
    - `/api/users/` (GET, POST)
    - `/api/users/user-todos` (GET)
    - `/api/users/<int:pk>/` (GET, PUT, PATCH, DELETE)

- **Todo Endpoints:**
    - `/api/todos/` (GET, POST)
    - `/api/todos/<int:pk>/` (GET, PUT, PATCH, DELETE)

## API Documentation - (Postman Collection)
You can find the API documentation at the following link: [API Documentation](https://www.postman.com/yunusemre482/workspace/n2mobile)

