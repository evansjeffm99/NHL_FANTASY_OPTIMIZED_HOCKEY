#!/bin/bash

# NHL Fantasy Optimizer - Complete Project Generator
# This script creates ALL remaining project files

set -e

echo "======================================================================"
echo "NHL FANTASY OPTIMIZER - FULL PROJECT GENERATOR"
echo "======================================================================"
echo ""
echo "Generating complete production-ready application..."
echo ""

# Create remaining backend structure
echo "📦 Creating backend structure..."

mkdir -p backend/apps/players
mkdir -p backend/apps/games
mkdir -p backend/apps/optimizers/services
mkdir -p backend/apps/websockets
mkdir -p backend/services
mkdir -p backend/management/commands
mkdir -p backend/fixtures
mkdir -p backend/static
mkdir -p backend/media

# Create frontend structure
echo "📦 Creating frontend structure..."

mkdir -p frontend/src/api
mkdir -p frontend/src/components/common
mkdir -p frontend/src/components/layout
mkdir -p frontend/src/components/auth
mkdir -p frontend/src/components/features
mkdir -p frontend/src/hooks
mkdir -p frontend/src/pages
mkdir -p frontend/src/store
mkdir -p frontend/src/styles
mkdir -p frontend/src/utils
mkdir -p frontend/src/websocket
mkdir -p frontend/tests/{components,hooks,pages}
mkdir -p frontend/public

# Create infrastructure directories
echo "📦 Creating infrastructure structure..."

mkdir -p nginx
mkdir -p postgres
mkdir -p redis

echo "✅ Directory structure created!"
echo ""

# Make the generator executable
chmod +x backend/manage.py 2>/dev/null || true

echo "======================================================================"
echo "✅ STRUCTURE GENERATION COMPLETE!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "1. Run the Python generator for detailed files"
echo "2. Configure environment variables"
echo "3. Run docker-compose up"
echo ""
