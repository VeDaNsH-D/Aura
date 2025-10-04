# Aura: Campus Safety and Alert System

Aura is a comprehensive campus safety and alert system designed to enhance the security and well-being of students and staff on a university campus. It provides real-time event tracking, entity management, and an alert system for inactive entities.

## Features

*   **Real-time Event Tracking**: Monitor events happening across the campus.
*   **Entity Management**: Keep track of all entities (e.g., security cameras, personnel) on campus.
*   **Identifier Management**: Assign and manage unique identifiers for each entity.
*   **Inactive Entity Alerts**: Automatically get notified when an entity has been inactive for a specified duration.
*   **RESTful API**: A well-documented API for interacting with the system.
*   **Asynchronous Task Processing**: Celery and Redis are used for handling background tasks like sending alerts.
*   **Containerized Deployment**: The entire application is containerized using Docker for easy setup and deployment.

## Tech Stack

*   **Backend**: Flask, Flask-RESTx, SQLAlchemy
*   **Frontend**: React
*   **Database**: PostgreSQL
*   **Asynchronous Tasks**: Celery, Redis
*   **Web Server**: Gunicorn, Nginx
*   **Containerization**: Docker, Docker Compose

## Architecture

The application is built on a microservices-oriented architecture and containerized using Docker Compose.

*   **Backend**: A Flask application that serves the RESTful API. It uses Gunicorn as the WSGI server.
*   **Frontend**: A React single-page application (SPA) served by Nginx.
*   **Database**: A PostgreSQL database for persistent storage.
*   **Celery**: Used for running asynchronous background tasks. It consists of:
    *   **Redis**: The message broker that queues tasks for Celery.
    *   **Worker**: A Celery worker that executes the tasks.
    *   **Beat**: A Celery beat scheduler for periodic tasks.

All services are connected via a custom bridge network.

## Prerequisites

*   Docker
*   Docker Compose

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Aura
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the `Aura/` directory by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your desired configuration, especially the PostgreSQL credentials.

3.  **Build and run the application:**
    ```bash
    docker-compose up --build
    ```
    This command will build the images for all services and start the containers.

4.  **Access the application:**
    *   **Frontend**: `http://localhost:3000`
    *   **Backend API**: `http://localhost:5000/api/`

5.  **(Optional) Seed the database:**
    To populate the database with some initial sample data, run the seeding script:
    ```bash
    docker-compose exec backend python scripts/seed_database.py
    ```

## Project Structure

```
Aura/
├── backend/
│   ├── app/                  # Main Flask application
│   │   ├── api/              # API blueprint, DTOs, and resources
│   │   ├── tasks/            # Celery tasks
│   │   ├── __init__.py       # Application factory
│   │   └── models.py         # SQLAlchemy models
│   ├── scripts/              # Helper scripts (e.g., seeding)
│   ├── celery_worker.py      # Celery application entry point
│   ├── config.py             # Application configuration
│   ├── Dockerfile            # Dockerfile for the backend
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── public/
│   ├── src/                  # React source code
│   ├── Dockerfile            # Dockerfile for the frontend
│   └── package.json          # Node.js dependencies
├── .env.example              # Example environment variables
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # This file
```

## Configuration

Application configuration is managed via environment variables. Create a `.env` file in the project root and set the following variables:

| Variable | Description | Default |
| --- | --- | --- |
| `POSTGRES_USER` | PostgreSQL username | `user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `password` |
| `POSTGRES_DB` | PostgreSQL database name | `campus_db` |
| `DATABASE_URL` | Full database connection string | `postgresql://user:password@db:5432/campus_db` |
| `CELERY_BROKER_URL` | URL for the Celery message broker | `redis://redis:6379/0` |
| `CELERY_RESULT_BACKEND` | URL for the Celery result backend | `redis://redis:6-alpine/0` |

## Database

The application uses PostgreSQL as its database and SQLAlchemy as the ORM. Database migrations are handled by Flask-Migrate.

*   **To apply migrations:**
    ```bash
    docker-compose exec backend flask db upgrade
    ```

*   **To create a new migration:**
    ```bash
    docker-compose exec backend flask db migrate -m "Your migration message"
    ```

## Asynchronous Tasks

Asynchronous tasks are managed by Celery.

*   **Task Definitions**: Tasks are defined in the `Aura/backend/app/tasks/` directory.
*   **Running the Worker**: The Celery worker is started as part of the `docker-compose up` command. You can also run it manually:
    ```bash
    docker-compose exec backend celery -A celery_worker.celery worker --loglevel=info
    ```
*   **Running the Beat Scheduler**: The Celery beat scheduler for periodic tasks is also started with `docker-compose up`. To run it manually:
    ```bash
    docker-compose exec backend celery -A celery_worker.celery beat --loglevel=info
    ```
