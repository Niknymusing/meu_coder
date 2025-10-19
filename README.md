# FastAPI Web Application

A production-ready FastAPI web application with multiple endpoints, proper validation, error handling, comprehensive tests, and CI/CD integration.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Pydantic Validation**: Automatic request/response validation
- **Error Handling**: Custom error handlers with meaningful responses
- **RESTful API**: Complete CRUD operations for Users and Items
- **Comprehensive Tests**: Unit and integration tests with pytest
- **CI/CD Pipeline**: GitHub Actions workflows for testing and deployment
- **Docker Support**: Multi-stage Dockerfile and docker-compose setup
- **Code Quality**: Black, Ruff, and MyPy for formatting and linting
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## Project Structure

```
fastapi-webapp/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   ├── endpoints/          # API route handlers
│   │   │   ├── health.py       # Health check endpoint
│   │   │   ├── users.py        # User CRUD operations
│   │   │   └── items.py        # Item CRUD operations
│   │   └── schemas/            # Pydantic models
│   │       ├── user.py
│   │       └── item.py
│   ├── core/
│   │   └── config.py           # Application configuration
│   └── middleware/
│       └── error_handler.py    # Error handling middleware
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── test_health.py
│   ├── test_users.py
│   └── test_items.py
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline
│       └── cd.yml              # CD pipeline
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata and tool configs
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker compose configuration
├── Makefile                    # Common commands
└── README.md
```

## Requirements

- Python 3.11 or higher
- pip

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-webapp
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Or use make
make install
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Local Development

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using make
make run
```

The application will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Using Docker

```bash
# Build and run with docker-compose
make docker-run

# Or manually
docker-compose up -d

# Stop containers
make docker-stop
```

## API Endpoints

### Health Check

- `GET /api/health` - Check API health status

### Users

- `POST /api/users/` - Create a new user
- `GET /api/users/` - Get all users (paginated)
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

### Items

- `POST /api/items/` - Create a new item
- `GET /api/items/` - Get all items (paginated, filterable)
- `GET /api/items/{item_id}` - Get item by ID
- `PUT /api/items/{item_id}` - Update item
- `DELETE /api/items/{item_id}` - Delete item

## Testing

### Run all tests

```bash
# Using pytest directly
pytest tests/ -v --cov=app --cov-report=html

# Or using make
make test
```

### View coverage report

After running tests, open `htmlcov/index.html` in your browser.

## Code Quality

### Format code

```bash
# Format with black
black app/ tests/

# Or using make
make format
```

### Run linters

```bash
# Lint with ruff
ruff check app/ tests/

# Type check with mypy
mypy app/

# Or using make
make lint
```

## Development

### Available Make commands

```bash
make help          # Show all available commands
make install       # Install production dependencies
make dev           # Install development dependencies
make test          # Run tests with coverage
make lint          # Run linters
make format        # Format code
make clean         # Clean up cache files
make run           # Run development server
make docker-build  # Build Docker image
make docker-run    # Run with docker-compose
make docker-stop   # Stop docker containers
```

## CI/CD

This project uses GitHub Actions for CI/CD:

### Continuous Integration (CI)

- Runs on push and pull requests to `main` and `develop` branches
- Tests on Python 3.11 and 3.12
- Runs linters (ruff, black)
- Type checking with mypy
- Unit and integration tests
- Code coverage reporting

### Continuous Deployment (CD)

- Triggers on push to `main` or version tags
- Builds and pushes Docker images
- Can be extended with deployment steps

## Configuration

Application configuration is managed through environment variables. See `.env.example` for available options:

- `ENVIRONMENT`: Application environment (development/production)
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Secret key for security features
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: CORS allowed hosts

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use Ruff for linting
- Add type hints where possible
- Write tests for new features

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

Future enhancements planned:

- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Authentication and authorization (JWT)
- [ ] Rate limiting
- [ ] Caching with Redis
- [ ] Background tasks with Celery
- [ ] WebSocket support
- [ ] GraphQL endpoint
- [ ] Prometheus metrics
- [ ] Logging and monitoring

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [Pytest](https://pytest.org/) - Testing framework
