# NHL Fantasy Optimizer - Deployment Guide

## Quick Start (5 Minutes)

### Prerequisites
- Docker Desktop installed and running
- Git installed
- 8GB RAM minimum
- 10GB free disk space

### Step-by-Step Setup

#### 1. Clone and Navigate
```bash
cd NHL_FANTASY_OPTIMIZED_HOCKEY
```

#### 2. Configure Environment Variables
```bash
# Backend configuration
cp backend/.env.example backend/.env

# Frontend configuration
cp frontend/.env.example frontend/.env

# (Optional) Edit .env files if needed
# nano backend/.env
```

#### 3. Build and Start All Services
```bash
docker-compose up -d --build
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache/queue (port 6379)
- Django backend (port 8000)
- Celery worker
- Celery beat scheduler
- React frontend (port 5173)
- Nginx reverse proxy (port 80)

#### 4. Run Database Migrations
```bash
docker-compose exec backend python manage.py migrate
```

#### 5. Create Admin User
```bash
docker-compose exec backend python manage.py createsuperuser
```

Follow the prompts to create your admin account.

#### 6. Load Demo Data (Optional)
```bash
docker-compose exec backend python manage.py loaddata fixtures/teams.json
```

#### 7. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/

---

## Verification Steps

### 1. Check Services Status
```bash
docker-compose ps
```

All services should show "Up" status.

### 2. Check Backend Health
```bash
curl http://localhost:8000/api/teams/
```

Should return JSON response (may be empty initially).

### 3. Check Frontend
Open http://localhost:5173 in your browser. You should see the login page.

### 4. Check Celery Worker
```bash
docker-compose logs celery | tail -20
```

Should show "celery@... ready."

---

## Common Issues and Solutions

### Issue: Port Already in Use

**Solution**: Stop conflicting services or change ports in docker-compose.yml

```bash
# Check what's using port 5173
lsof -i :5173

# Kill the process or change the port
```

### Issue: Database Connection Error

**Solution**: Wait for PostgreSQL to fully start

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart backend after postgres is ready
docker-compose restart backend
```

### Issue: Frontend Can't Connect to Backend

**Solution**: Check CORS and API URL settings

```bash
# Edit frontend/.env
VITE_API_URL=http://localhost:8000

# Edit backend/.env
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Issue: Migrations Fail

**Solution**: Drop database and recreate

```bash
docker-compose down -v
docker-compose up -d postgres redis
sleep 10
docker-compose up -d backend
docker-compose exec backend python manage.py migrate
```

---

## Development Workflow

### Backend Development

```bash
# View backend logs
docker-compose logs -f backend

# Run backend tests
docker-compose exec backend pytest

# Access Django shell
docker-compose exec backend python manage.py shell

# Create new migration
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate
```

### Frontend Development

```bash
# View frontend logs
docker-compose logs -f frontend

# Install new NPM package
docker-compose exec frontend npm install <package-name>

# Run frontend tests
docker-compose exec frontend npm test

# Build for production
docker-compose exec frontend npm run build
```

### Database Operations

```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U nhl_user -d nhl_fantasy

# Backup database
docker-compose exec postgres pg_dump -U nhl_user nhl_fantasy > backup.sql

# Restore database
docker-compose exec -T postgres psql -U nhl_user nhl_fantasy < backup.sql
```

### Celery Tasks

```bash
# View Celery worker logs
docker-compose logs -f celery

# View Celery beat logs
docker-compose logs -f celery-beat

# Manually trigger a task
docker-compose exec backend python manage.py shell
>>> from apps.teams.tasks import update_standings_task
>>> update_standings_task.delay()
```

---

## Production Deployment

### Environment Variables for Production

Edit `backend/.env`:
```bash
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:password@db-host:5432/db_name
REDIS_URL=redis://redis-host:6379/0
```

### SSL/HTTPS Setup

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update nginx/nginx.conf with SSL configuration
3. Add certificates to nginx/certs/ directory

### Database Considerations

- Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
- Enable connection pooling
- Set up regular backups
- Configure read replicas for scaling

### Security Checklist

- [ ] Set DEBUG=False
- [ ] Generate strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL/HTTPS
- [ ] Enable firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Configure CORS properly
- [ ] Set up logging and monitoring
- [ ] Enable database backups
- [ ] Use strong passwords
- [ ] Limit database access

---

## Monitoring and Logs

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Django Logs Location
```
backend/logs/django.log
```

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    scale: 3  # Run 3 backend instances

  celery:
    scale: 5  # Run 5 celery workers
```

### Load Balancing

Update nginx.conf to distribute load:
```nginx
upstream backend {
    server backend_1:8000;
    server backend_2:8000;
    server backend_3:8000;
}
```

---

## Backup and Restore

### Backup Script
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U nhl_user nhl_fantasy > backup_$DATE.sql
tar -czf media_$DATE.tar.gz backend/media/
echo "Backup completed: backup_$DATE.sql and media_$DATE.tar.gz"
```

### Restore Script
```bash
#!/bin/bash
docker-compose exec -T postgres psql -U nhl_user nhl_fantasy < backup.sql
tar -xzf media.tar.gz -C backend/
echo "Restore completed"
```

---

## Updating the Application

### Pull Latest Changes
```bash
git pull origin main
```

### Rebuild and Restart
```bash
docker-compose down
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```

---

## Useful Commands Reference

```bash
# Start services
make up
# OR
docker-compose up -d

# Stop services
make down
# OR
docker-compose down

# View logs
make logs
# OR
docker-compose logs -f

# Run migrations
make migrate
# OR
docker-compose exec backend python manage.py migrate

# Create superuser
make createsuperuser
# OR
docker-compose exec backend python manage.py createsuperuser

# Run tests
make test
# OR
docker-compose exec backend pytest

# Clean everything (removes volumes)
make clean
# OR
docker-compose down -v
```

---

## Performance Tuning

### Backend
- Increase Gunicorn workers in Dockerfile
- Enable database query optimization
- Configure Redis maxmemory policy
- Use connection pooling

### Frontend
- Enable production build optimization
- Use CDN for static assets
- Enable Gzip compression
- Implement code splitting

### Database
- Add appropriate indexes
- Configure query caching
- Optimize slow queries
- Use database connection pooling

---

## Support and Troubleshooting

### Debug Mode
To enable detailed error messages during development:

```bash
# backend/.env
DEBUG=True
DJANGO_LOG_LEVEL=DEBUG
```

### Check Service Health
```bash
# Backend health
curl http://localhost:8000/api/teams/

# Redis health
docker-compose exec redis redis-cli ping

# PostgreSQL health
docker-compose exec postgres pg_isready -U nhl_user
```

### Reset Everything
If you need to start fresh:
```bash
docker-compose down -v  # Remove all volumes
rm -rf backend/__pycache__ backend/*/__pycache__
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

---

## Next Steps

1. Customize team logos and colors
2. Add more NHL API integrations
3. Implement additional optimizer features
4. Set up monitoring (Sentry, New Relic)
5. Configure CI/CD pipeline
6. Add email notifications
7. Implement user preferences
8. Create mobile responsive views

---

**Status**: Production Ready ✅
**Version**: 1.0.0
**Last Updated**: November 2025
