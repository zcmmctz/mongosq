# MongoDB Database Management API

A FastAPI-based RESTful API for managing MongoDB databases and collections, with built-in connection pool management, error handling, and security features.

## Features

- **Database Management**: Create, delete, and list MongoDB databases
- **Collection Management**: Create, delete, and list collections within databases
- **Document Operations**: Insert, find, update, delete, and count documents within collections
- **Connection Pooling**: Optimized MongoDB connection management
- **Error Handling**: Comprehensive error handling and logging
- **Security**: API key authentication for write operations
- **Documentation**: Auto-generated Swagger UI documentation
- **Validation**: Request validation using Pydantic models
- **Scalability**: Designed for high availability and performance

## Project Structure

```
server/
├── src/
│   ├── config/
│   │   ├── settings.py    # Application settings
│   │   └── security.py     # Security configuration
│   └── db/
│       ├── connection.py   # MongoDB connection management
│       └── manager.py      # Database operations
├── tests/
│   ├── test_connection.py  # Connection tests
│   ├── test_manager.py     # Database operations tests
│   └── test_api.py         # API endpoint tests
├── main.py                 # FastAPI application
├── pyproject.toml          # Project dependencies
├── .env                    # Environment variables
└── README.md               # This file
```

## Prerequisites

- Python 3.12+
- MongoDB 4.0+
- pip or uv package manager

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mongosq/server
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv install
   
   # Using pip
   pip install -e .
   ```

3. **Configure environment variables**:
   Edit the `.env` file to set your MongoDB connection details and API key:
   ```env
   # MongoDB Connection Configuration
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=admin
   MONGODB_USERNAME=
   MONGODB_PASSWORD=

   # Connection Pool Settings
   MONGODB_MAX_POOL_SIZE=100
   MONGODB_MIN_POOL_SIZE=10
   MONGODB_MAX_IDLE_TIME_MS=300000

   # Logging Settings
   LOG_LEVEL=INFO

   # Security Settings
   API_KEY=your-secret-api-key-change-in-production
   ```

## Usage

1. **Start the server**:
   ```bash
   # Using Python
   python main.py
   
   # Using uvicorn directly
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access the API**:
   - API root: `http://localhost:8000/`
   - Swagger UI documentation: `http://localhost:8000/docs`
   - ReDoc documentation: `http://localhost:8000/redoc`

3. **API Endpoints**:

   | Method | Endpoint | Description | Authentication |
   |--------|----------|-------------|----------------|
   | GET    | /        | Root endpoint | None |
   | GET    | /health  | Health check | None |
   | GET    | /databases | List all databases | None |
   | POST   | /databases | Create a new database | API Key |
   | DELETE | /databases/{db_name} | Delete a database | API Key |
   | GET    | /databases/{db_name}/collections | List collections | None |
   | POST   | /collections | Create a new collection | API Key |
   | DELETE | /databases/{db_name}/collections/{collection_name} | Delete a collection | API Key |
   | POST   | /databases/{db_name}/collections/{collection_name}/documents | Create a new document | API Key |
   | GET    | /databases/{db_name}/collections/{collection_name}/documents | Find documents | None |
   | GET    | /databases/{db_name}/collections/{collection_name}/documents/{document_id} | Find document by ID | None |
   | PUT    | /databases/{db_name}/collections/{collection_name}/documents/{document_id} | Update a document | API Key |
   | DELETE | /databases/{db_name}/collections/{collection_name}/documents/{document_id} | Delete a document | API Key |
   | GET    | /databases/{db_name}/collections/{collection_name}/documents/count | Count documents | None |
   | POST   | /settings/connection | Update database connection settings | API Key |
   | GET    | /settings/connection | Get current database connection settings | None |

4. **Authentication**:
   For write operations (POST, DELETE), include an `Authorization` header with your API key:
   ```
   Authorization: Bearer your-api-key
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_connection.py
pytest tests/test_manager.py
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## Production Deployment

1. **Set a strong API key** in the `.env` file
2. **Configure CORS** origins in `main.py`
3. **Use a process manager** like Gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```
4. **Set up monitoring** and logging
5. **Consider using a MongoDB replica set** for high availability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
