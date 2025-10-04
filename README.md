# Aura: Campus Safety and Alert System

<p align="center">
  <img src="https://raw.githubusercontent.com/OT-OS/Aura/main/Aura_logo.png" alt="Aura Logo" width="200"/>
</p>

<p align="center">
  <strong>A comprehensive campus safety and alert system designed to enhance the security and well-being of students and staff.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#api-documentation">API Documentation</a> •
  <a href="#database-migrations">Database Migrations</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

---

Aura is a robust and scalable solution for monitoring and managing campus safety. It provides real-time event tracking, entity management, and a proactive alert system to ensure a secure environment.

## Features

*   **Real-time Event Tracking**: Monitor events happening across the campus in real-time.
*   **Entity Management**: Keep a comprehensive record of all entities (e.g., security cameras, personnel, assets).
*   **Identifier Management**: Assign and manage unique identifiers for each entity for seamless tracking.
*   **Inactive Entity Alerts**: Automatically receive notifications when an entity has been inactive for a specified duration, ensuring operational readiness.
*   **RESTful API**: A well-documented and easy-to-use API for interacting with the system.
*   **Asynchronous Task Processing**: Leverages Celery and Redis for handling background tasks like sending alerts, ensuring the application remains responsive.
*   **Containerized Deployment**: The entire application is containerized using Docker for easy setup, deployment, and scalability.

## Tech Stack

| Component             | Technology                                       |
| --------------------- | ------------------------------------------------ |
| **Backend**           | Flask, Flask-RESTx, SQLAlchemy                   |
| **Frontend**          | React                                            |
| **Database**          | PostgreSQL                                       |
| **Asynchronous Tasks**| Celery, Redis                                    |
| **Web Server**        | Gunicorn, Nginx                                  |
| **Containerization**  | Docker, Docker Compose                           |

## Architecture

The application is built on a service-oriented architecture and is fully containerized using Docker Compose.

*   **Backend**: A Flask application that serves the RESTful API. It uses Gunicorn as the WSGI server.
*   **Frontend**: A React single-page application (SPA) served by Nginx.
*   **Database**: A PostgreSQL database for persistent data storage.
*   **Celery**: Used for running asynchronous background tasks. It consists of:
    *   **Redis**: The message broker that queues tasks for Celery.
    *   **Worker**: A Celery worker that executes the tasks.
    *   **Beat**: A Celery beat scheduler for periodic tasks (e.g., checking for inactive entities).

All services are connected via a custom bridge network, ensuring secure and efficient communication.

## Getting Started

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/OT-OS/Aura.git
    cd Aura
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the `Aura/` directory by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your desired configuration, especially the PostgreSQL credentials.

3.  **Build and Run the Application:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for all services and start the containers.

4.  **Access the Application:**
    *   **Frontend**: `http://localhost:3000`
    *   **Backend API**: `http://localhost:5000/api/`

5.  **(Optional) Seed the Database:**
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
│   │   ├── services/         # Business logic
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

Application configuration is managed via environment variables. Create a `.env` file in the project root and set the variables as needed.

| Variable              | Description                              | Default                                    |
| --------------------- | ---------------------------------------- | ------------------------------------------ |
| `POSTGRES_USER`       | PostgreSQL username                      | `user`                                     |
| `POSTGRES_PASSWORD`   | PostgreSQL password                      | `password`                                 |
| `POSTGRES_DB`         | PostgreSQL database name                 | `campus_db`                                |
| `DATABASE_URL`        | Full database connection string          | `postgresql://user:password@db:5432/campus_db` |
| `CELERY_BROKER_URL`   | URL for the Celery message broker        | `redis://redis:6379/0`                     |
| `CELERY_RESULT_BACKEND` | URL for the Celery result backend        | `redis://redis:6379/0`                     |
| `SECRET_KEY`          | Secret key for Flask application         | `a_very_secret_key`                        |

## API Documentation

The API is documented using Flask-RESTx and is accessible at the `/api/` endpoint once the application is running. The documentation provides a list of available endpoints, HTTP methods, request/response formats, and allows for interactive API testing.

**API Base URL**: `http://localhost:5000/api/`

## Database Migrations

Database migrations are managed using Flask-Migrate.

*   **To apply migrations:**
    ```bash
    docker-compose exec backend flask db upgrade
    ```

*   **To create a new migration (after model changes):**
    ```bash
    docker-compose exec backend flask db migrate -m "A descriptive migration message"
    ```
    This will generate a new migration script in the `migrations/` directory.

## Future Improvements

For a detailed list of suggested enhancements and future development plans, please see the [IMPROVEMENTS.md](IMPROVEMENTS.md) file.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to contribute to the project, please follow these steps:

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.