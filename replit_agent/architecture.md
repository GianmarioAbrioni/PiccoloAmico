# Architecture Overview

## 1. Overview

This repository contains a Dog Breeding Management System called "Piccolo Amico". It's a web application designed to help dog breeders track and manage their breeding operations, including information about dogs, vaccinations, matings, births, and related statistics.

The system is built as a server-rendered web application following a traditional monolithic architecture. It uses Flask as the web framework and SQLAlchemy as the ORM for database interactions.

## 2. System Architecture

The application follows a classic Model-View-Controller (MVC) architecture:

- **Models**: Defined using SQLAlchemy ORM, representing database entities like dogs, vaccinations, matings, and births
- **Views**: Implemented as Flask routes that handle HTTP requests and responses
- **Templates**: HTML files with Jinja2 templating for rendering the UI
- **Controllers**: Logic embedded in Flask route handlers

The system is designed as a monolithic application where all components run in a single process. This architecture was chosen for simplicity of development and deployment.

```
┌─────────────────────────────────────┐
│               Client                │
│        (Web Browser/Device)         │
└───────────────────┬─────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│           Web Application           │
│         (Flask + Templates)         │
└───────────────────┬─────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│        Database (PostgreSQL)        │
└─────────────────────────────────────┘
```

## 3. Key Components

### 3.1. Backend (Python/Flask)

The backend is built with Flask, a lightweight web framework for Python. It handles:

- Routing and request processing
- Database operations via SQLAlchemy
- Template rendering
- Business logic
- PDF generation using pdfkit

Key files:
- `app.py`: Main application setup and configuration
- `models.py`: Database models and relationships
- `routes.py`: URL routing and request handling logic
- `utils.py`: Utility functions

### 3.2. Database Schema

The application uses SQLAlchemy ORM with a relational database (PostgreSQL in production, SQLite for development). The main entities are:

- **Dog**: Core entity with attributes like name, breed, microchip details, gender, birth date, etc.
- **Vaccination**: Tracks vaccinations given to dogs
- **Mating**: Records breeding events between dogs
- **Birth**: Tracks birth events, connected to matings

Key relationships:
- Dogs have parent-child relationships (mother/father references)
- Dogs have one-to-many relationships with vaccinations
- Dogs have many-to-many relationships through matings
- Female dogs have one-to-many relationships with births

### 3.3. Frontend

The frontend is built using server-side rendering with Jinja2 templates:

- Bootstrap CSS framework for styling
- Font Awesome for icons
- Chart.js for data visualization
- Simple JavaScript for interactive elements

The templates are organized by feature area:
- Layout templates for consistent UI structure
- Feature-specific templates (dogs, vaccinations, matings, births)
- PDF generation templates

## 4. Data Flow

1. **HTTP Request**: Client sends a request to a specific route
2. **Route Handler**: Flask processes the request in the appropriate route handler
3. **Database Operations**: SQLAlchemy models query or modify the database
4. **Template Rendering**: Results are passed to Jinja2 templates
5. **HTTP Response**: Rendered HTML is sent back to the client

For data modification flows (create, update, delete):
1. Form submission from the client
2. Server-side validation
3. Database operations
4. Redirect to a relevant page with a success/error message

## 5. External Dependencies

The application relies on several external libraries and services:

### 5.1. Main Dependencies

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Gunicorn**: WSGI HTTP server for production deployment
- **Bootstrap**: CSS framework for UI components
- **pdfkit/wkhtmltopdf**: PDF generation
- **pandas**: Data processing for reports
- **openpyxl**: Excel file handling

### 5.2. Development Dependencies

- **email-validator**: Validation of email addresses
- **psycopg2-binary**: PostgreSQL driver

## 6. Deployment Strategy

The application is designed to be deployed to cloud platforms:

### 6.1. Production Setup

The system uses:
- **Gunicorn** as the WSGI HTTP server
- **PostgreSQL** as the production database
- Configuration through environment variables

### 6.2. Deployment Process

Deployment is configured for:
- **Autoscaling environment**: The `.replit` file indicates a deployment setup with autoscaling
- **Web Worker Configuration**: Gunicorn is configured with workers and threads
- **Database Initialization**: The `build.sh` script creates the initial database tables

### 6.3. Environment Configuration

The application uses environment variables for configuration:
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Secret key for session management
- `PORT`: Port to run the web server on

### 6.4. Containerization

While not explicitly defined in the repository, the presence of a `build.sh` script and `Procfile` suggests the application may be containerized for deployment, likely using Render or a similar platform that supports PostgreSQL.

## 7. Secondary Application (PiccoloAmico)

There is a secondary "PiccoloAmico" application within the repository that appears to be an earlier or alternative version. It has a similar architecture but is structured differently and has some API endpoints, suggesting it might support a separate frontend.

This secondary application isn't integrated with the main application and might be kept for reference or future development.