# FastAPI Project

A FastAPI application with MySQL database, JWT authentication, and role-based access control.

## Features

- **RESTful API Endpoints** - CRUD operations for books
- **JWT Authentication** - Secure login/signup with JSON Web Tokens
- **Role-Based Access Control** - User and admin dashboards
- **MySQL Database** - Persistent data storage with SQLAlchemy ORM
- **Docker Support** - Containerized application with docker-compose

## Project Structure

```
fastapi/
├── auth/                    # Authentication module
│   ├── main.py             # Auth endpoints (signup, login, protected routes)
│   ├── model.py            # User SQLAlchemy model
│   ├── schemas.py          # Pydantic schemas
│   ├── utils.py            # Password hashing utilities
│   └── auth_database.py    # Database connection
├── main.py                 # Basic FastAPI app
├── crud.py                 # Book CRUD operations
├── model.py                # Book database model
├── database.py             # Database configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Docker Compose configuration
└── init.sql               # MySQL initialization script
```

## Requirements

- Python 3.13+
- MySQL 8.0
- Docker & Docker Compose

## Installation

### Option 1: Pull Pre-built Image
```bash
# Pull the Docker image
docker pull adamya2307/fastapi@sha256:9b261e2eebfab5f142774c0ed31601af5d1c225fe7a14e3f9b3f34adff7aed60

# Run standalone (requires external MySQL)
docker run -d -p 8000:8000 \
  -e MYSQL_HOST=<mysql_host> \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=0000 \
  -e MYSQL_DATABASE=fast_api \
  --name fastapi_app adamya2307/fastapi@sha256:9b261e2eebfab5f142774c0ed31601af5d1c225fe7a14e3f9b3f34adff7aed60

# Or run with MySQL using docker-compose
docker compose up
```

### Option 2: Build from Source
```bash
docker compose up --build
```

### Option 3: Local Development
```bash
pip install -r requirements.txt
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MYSQL_HOST | db | Database host |
| MYSQL_PORT | 3306 | Database port |
| MYSQL_USER | root | Database user |
| MYSQL_PASSWORD | 0000 | Database password |
| MYSQL_DATABASE | fast_api | Database name |

## API Endpoints

### Basic API (main.py)
- `GET /` - Welcome message
- `GET /about` - About page
- `GET /greet/?name={name}&age={age}` - Greeting endpoint

### Book CRUD (crud.py)
- `GET /all/` - Get all books
- `GET /get_by_books?id={id}` - Get book by ID
- `GET /book/{id}` - Get book by ID (path)
- `POST /add/book` - Add new book
- `PUT /update/{id}` - Update book
- `DELETE /delete/book/{id}` - Delete book

### Authentication (auth/main.py)
- `GET /` - Welcome HTML page
- `POST /signup` - Register new user
- `POST /login` - Login and get JWT token
- `GET /protected` - Protected route (requires auth)
- `GET /profile` - Profile (user/admin role)
- `GET /user/dashboard` - User dashboard
- `GET /admin/dashboard` - Admin dashboard

## Running the Application

### Using Docker:
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`

### Using uvicorn directly:
```bash
uvicorn main:app --reload
# or for auth module
uvicorn auth.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication Flow

1. **Signup:** POST to `/signup` with username, email, password, role
2. **Login:** POST to `/login` with username and password
3. **Access Protected Routes:** Include JWT token in Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```

## Database

The application uses MySQL 8.0. Tables are auto-created on startup via SQLAlchemy.