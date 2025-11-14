# NHL Fantasy Optimizer

Production-ready NHL Fantasy Hockey optimization and analytics platform.

## Features

- **JWT Authentication** - Secure user authentication with token refresh
- **NHL Data Integration** - Real-time data from NHL API
- **Schedule Analyzer** - Advanced fantasy week analysis
- **Monte Carlo Simulation** - Win probability and power rankings
- **WebSocket Support** - Real-time updates
- **Celery Tasks** - Automated data fetching and processing
- **Docker Deployment** - Complete containerized stack

## Tech Stack

### Backend
- Django 4.2 + Django REST Framework
- PostgreSQL database
- Redis for caching and message queue
- Celery for background tasks
- Django Channels for WebSockets
- JWT authentication

### Frontend
- React 18 with Vite
- Ant Design UI library
- Redux Toolkit for state management
- Axios with auto-refresh interceptors
- React Router for navigation

### Infrastructure
- Docker Compose orchestration
- Nginx reverse proxy
- PostgreSQL database
- Redis cache/queue

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NHL_FANTASY_OPTIMIZED_HOCKEY
```

2. Copy environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Build and start services:
```bash
docker-compose up -d --build
```

4. Run migrations:
```bash
docker-compose exec backend python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Load demo data (optional):
```bash
docker-compose exec backend python manage.py loaddata fixtures/teams.json
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/

## Development

### Backend Development

```bash
# Run migrations
make migrate

# Create superuser
make createsuperuser

# Run tests
make test

# Open Django shell
make shell

# View logs
make logs
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user

### Teams
- `GET /api/teams/` - List all teams
- `GET /api/teams/{id}/` - Get team details
- `GET /api/teams/standings/` - Get current standings

### Players
- `GET /api/players/` - List all players
- `GET /api/players/{id}/` - Get player details

### Games
- `GET /api/games/` - List games
- `GET /api/games/{id}/` - Get game details

### Optimizers
- `POST /api/optimizers/schedule-analysis/analyze/` - Analyze schedule
- `POST /api/optimizers/schedule-analysis/monte_carlo/` - Run Monte Carlo simulation

## Architecture

```
nhl-fantasy-optimizer/
├── backend/              # Django backend
│   ├── core/            # Django settings and configuration
│   ├── apps/            # Django applications
│   │   ├── authentication/
│   │   ├── teams/
│   │   ├── players/
│   │   ├── games/
│   │   ├── optimizers/
│   │   └── websockets/
│   └── services/        # Business logic services
├── frontend/            # React frontend
│   ├── src/
│   │   ├── api/        # API clients
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── store/      # Redux store
│   │   └── hooks/      # Custom hooks
│   └── public/
├── nginx/              # Nginx configuration
└── docker-compose.yml  # Docker orchestration
```

## Environment Variables

See `backend/.env.example` and `frontend/.env.example` for all available configuration options.

## Testing

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
cd frontend && npm test
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in backend/.env
2. Configure proper `SECRET_KEY`
3. Set up SSL certificates
4. Configure allowed hosts
5. Use production WSGI server (Gunicorn)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
