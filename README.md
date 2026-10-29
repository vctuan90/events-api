# STRAUMANN Event API

FastAPI backend for STRAUMANN Event Management System with PostgreSQL, Redis, and modern async/await architecture.

## 🚀 Features

- **FastAPI** - Modern, fast (high-performance) web framework
- **PostgreSQL** - Robust relational database
- **Redis** - Caching and session storage
- **SQLAlchemy 2.0** - Modern ORM with async support
- **Alembic** - Database migrations
- **JWT Authentication** - Secure token-based auth
- **WebSocket** - Real-time communication for live sessions
- **Docker** - Containerized deployment
- **Structured Logging** - JSON logging with structlog
- **Auto-generated API docs** - OpenAPI/Swagger

## 📋 Requirements

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create environment file**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Option 2: Hybrid Development (Recommended for Coding) 🔥

**Backend runs locally + Services in Docker**

1. **Start Docker Services**
   ```bash
   docker compose -f docker-compose.services.yml up -d
   ```

2. **Setup Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Environment & Database**
   ```bash
   cp env.local .env
   alembic upgrade head
   ```

4. **Start Backend**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Seed Sample Data (Optional)**
   ```bash
   python seed_database.py
   ```

**Services Available:**
- **PostgreSQL**: localhost:5432 (straumann/password)
- **Redis**: localhost:6379

## 🗄️ Database Schema

The application includes complete database models for:

- **Users** - User accounts with JWT authentication
- **Events** - Event management
- **Sessions** - Event sessions with live support
- **Speakers** - Speaker profiles and session assignments
- **Favorites** - User favorites system
- **Gallery** - Image gallery with approval workflow
- **Notifications** - Push notification system
- **Networking** - User connection system
- **Surveys** - Dynamic survey system
- **Products** - Neodent product catalog
- **Badges** - Gamification system
- **Digital Certificates** - Certificate management

## 🌱 Sample Data

The project includes a comprehensive seed data script to populate your database with realistic sample data for development and testing.

### Quick Start with Sample Data

```bash
# Run migrations first
alembic upgrade head

# Seed the database
python seed_database.py
```

### 👥 Sample Login Accounts

After seeding, you can use these accounts to test the API:

**Admin Account:**
- Email: `admin@straumann.com`
- Password: `admin123`
- Role: Admin (full access)

**Regular User Accounts:**
- Email: `john.doe@example.com` / Password: `user123` (Dentist)
- Email: `jane.smith@example.com` / Password: `user123` (Oral Surgeon)
- Email: `mike.wilson@example.com` / Password: `user123` (Professor/Speaker)
- Email: `sarah.johnson@example.com` / Password: `user123` (Event Organizer)
- Email: `david.brown@example.com` / Password: `user123` (Dental Technician)

### 📊 Sample Data Includes

- **3 Events** - Digital Dentistry Summit, Neodent Workshop, Virtual Masterclass
- **5 Sessions** - Various session types (scheduled, live, workshop)
- **4 Speakers** - Expert profiles with bios and credentials
- **4 Neodent Products** - Implant systems and instruments
- **User Interactions** - Favorites, registrations, notifications
- **Badges & Static Pages** - Gamification and content pages

## 🔧 Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1

# View migration history
alembic history
```

## 🔑 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register a user**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login`
3. **Get access token** and include it in headers:
   ```
   Authorization: Bearer <your-access-token>
   ```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user

#### Events
- `GET /api/v1/events/` - List all events (with pagination)
- `POST /api/v1/events/` - Create new event (Admin only)
- `GET /api/v1/events/{id}` - Get event details
- `PUT /api/v1/events/{id}` - Update event (Admin only)
- `DELETE /api/v1/events/{id}` - Delete event (Admin only)
- `GET /api/v1/events/{id}/sessions` - Get event sessions

#### Sessions
- `GET /api/v1/sessions/` - List all sessions (with filtering)
- `POST /api/v1/sessions/` - Create new session (Admin only)
- `GET /api/v1/sessions/{id}` - Get session details
- `PUT /api/v1/sessions/{id}` - Update session (Admin only)
- `DELETE /api/v1/sessions/{id}` - Delete session (Admin only)
- `POST /api/v1/sessions/{id}/register` - Register for session
- `DELETE /api/v1/sessions/{id}/register` - Unregister from session
- `GET /api/v1/sessions/{id}/participants` - Get session participants (Admin only)

#### Speakers
- `GET /api/v1/speakers/` - List all speakers (with pagination)
- `POST /api/v1/speakers/` - Create new speaker (Admin only)
- `GET /api/v1/speakers/{id}` - Get speaker details
- `PUT /api/v1/speakers/{id}` - Update speaker (Admin only)
- `DELETE /api/v1/speakers/{id}` - Delete speaker (Admin only)

#### Favorites
- `GET /api/v1/favorites/` - Get user's favorites
- `POST /api/v1/favorites/` - Add to favorites
- `DELETE /api/v1/favorites/{id}` - Remove from favorites

## 🌐 WebSocket Support

Real-time features for live sessions:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/sessions/{session_id}');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Live update:', data);
};
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start only database services
docker-compose up postgres redis

# View logs
docker-compose logs api

# Run migrations in container
docker-compose exec api alembic upgrade head

# Access container shell
docker-compose exec api bash

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📊 Monitoring & Logging

- **Health Check**: `GET /health`
- **Structured JSON Logging** with request tracking
- **Performance Headers** - X-Process-Time in responses
- **Error Handling** - Comprehensive error responses

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 🔒 Security Features

- **JWT Authentication** with refresh tokens
- **Password hashing** with bcrypt
- **CORS configuration**
- **Input validation** with Pydantic
- **SQL injection protection** with SQLAlchemy
- **Rate limiting** (to be implemented)

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/           # Core functionality (config, security, database)
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── crud/           # Database operations
│   ├── api/            # API endpoints
│   └── utils/          # Utility functions
├── alembic/            # Database migrations
├── uploads/            # File uploads directory
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker services
├── Dockerfile         # Application container
└── README.md          # This file
```

## 🚀 Deployment

### Production with Docker

1. **Update environment variables**
   ```bash
   # Set production values in .env
   DEBUG=False
   SECRET_KEY=<strong-secret-key>
   DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
   ```

2. **Build and deploy**
   ```bash
   docker-compose -f docker-compose.yml --profile production up -d
   ```

3. **Run migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Async PostgreSQL connection string | Required |
| `DATABASE_URL_SYNC` | Sync PostgreSQL for migrations | Required |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT secret key | Auto-generated |
| `DEBUG` | Enable debug mode | `False` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.