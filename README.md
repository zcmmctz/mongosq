# mongosq

MongoDB Web Management Tool - A comprehensive web-based interface for managing MongoDB databases.

## Features

- ✅ Database management (create, list, delete)
- ✅ Collection management (create, list, delete)
- ✅ Document operations (create, read, update, delete)
- ✅ User authentication with JWT
- ✅ Docker deployment support
- ✅ Responsive web interface
- ✅ API for programmatic access

## System Requirements

- **Frontend**: Node.js 20+
- **Backend**: Python 3.12+
- **Python Package Manager**: uv (recommended) or pip
- **Database**: MongoDB 4.0+
- **Docker**: Optional, for containerized deployment

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd mongosq
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

### 3. Backend Setup

```bash
cd server
# Install with uv (recommended)
uv add -e .

# Or with pip (alternative)
pip install -e .
```

## Configuration

### Backend Configuration

Edit the `.env` file in the `server` directory:

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

# account & password
ACCOUNT=admin
PASSWORD=your-password-change-in-production
```

### Frontend Configuration

Edit the `quasar.config.ts` file in the `frontend` directory to customize development server settings:

```typescript
devServer: {
  open: true,
  proxy: {
    '/api': {
      target: 'http://localhost:22222',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    },
    '/login': {
      target: 'http://localhost:22222',
      changeOrigin: true
    }
    // Add other endpoints as needed
  }
}
```

## Usage

### Development Mode

1. **Start the backend server**:

```bash
cd server
python main.py
```

The backend will run on `http://localhost:22222`

2. **Start the frontend development server**:

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:9000` (or the next available port)

### Production Deployment

#### Option 1: Docker Deployment

```bash
docker-compose up -d
```

The application will be available at `http://localhost:22222`

#### Option 2: Manual Deployment

1. **Build the frontend**:

```bash
cd frontend
npm run build
```

2. **Copy the built frontend to the backend**:

```bash
cp -r frontend/dist/spa/* server/static/
```

3. **Start the backend server**:

```bash
cd server
python main.py
```

The application will be available at `http://localhost:22222`

## Login

1. Open the application in your browser
2. You will be redirected to the login page
3. Enter your credentials:
   - **Username**: The value of `ACCOUNT` from `server/.env` (default: `admin`)
   - **Password**: The value of `PASSWORD` from `server/.env` (default: `your-password-change-in-production`)
4. Click "Login" to access the main dashboard

## Basic Operations

### Managing Databases
1. Navigate to the "Databases" page
2. **Create**: Enter a database name and click "Create"
3. **List**: All databases will be displayed in a table
4. **Delete**: Click the delete button next to a database

### Managing Collections
1. Navigate to the "Collections" page
2. Select a database from the dropdown
3. **Create**: Enter a collection name and click "Create"
4. **List**: All collections in the selected database will be displayed
5. **Delete**: Click the delete button next to a collection

### Managing Documents
1. Navigate to the "Documents" page
2. Select a database and collection
3. **Create**: Enter document data in JSON format and click "Create"
4. **List**: All documents in the selected collection will be displayed
5. **Update**: Click the edit button next to a document, make changes, and save
6. **Delete**: Click the delete button next to a document

## API Documentation

Once the backend is running, you can access the API documentation at:

- Swagger UI: `http://localhost:22222/docs`
- ReDoc: `http://localhost:22222/redoc`

### Key API Endpoints

- **POST /login**: User authentication
- **GET /databases**: List all databases
- **POST /databases**: Create a new database
- **DELETE /databases/{db_name}**: Delete a database
- **GET /databases/{db_name}/collections**: List collections in a database
- **POST /collections**: Create a new collection
- **DELETE /databases/{db_name}/collections/{collection_name}**: Delete a collection
- **GET /databases/{db_name}/collections/{collection_name}/documents**: List documents
- **POST /databases/{db_name}/collections/{collection_name}/documents**: Create a document
- **PUT /databases/{db_name}/collections/{collection_name}/documents/{document_id}**: Update a document
- **DELETE /databases/{db_name}/collections/{collection_name}/documents/{document_id}**: Delete a document

## Docker Configuration

The project includes Docker support for easy deployment:

- **Dockerfile**: Multi-stage build for both frontend and backend
- **docker-compose.yml**: Simplified deployment configuration

### Docker Environment Variables

You can override the default environment variables in `docker-compose.yml`:

```yaml
environment:
  - MONGODB_URI=mongodb://localhost:27017
  - MONGODB_DB_NAME=admin
```

## Troubleshooting

### Common Issues

1. **Backend server not starting**:
   - Check if MongoDB is running
   - Verify the `MONGODB_URI` in `.env` is correct
   - Ensure all Python dependencies are installed

2. **uv command not found**:
   - Install uv: `pip install uv`
   - Or use pip as an alternative: `pip install -e .`

3. **Frontend can't connect to backend**:
   - Verify the backend is running on port 22222
   - Check the proxy configuration in `quasar.config.ts`
   - Ensure CORS is properly configured

4. **Login failed**:
   - Verify the `ACCOUNT` and `PASSWORD` in `.env` are correct
   - Check the browser console for error messages
   - Verify the backend is receiving the login request

5. **Docker deployment issues**:
   - Ensure Docker is running
   - Check if port 22222 is available
   - Verify MongoDB connection from the container

## Security Considerations

- **API Key**: Change the `API_KEY` in `.env` to a strong, unique value
- **Credentials**: Change the default `ACCOUNT` and `PASSWORD` in `.env`
- **CORS**: In production, restrict `CORS_ALLOW_ORIGIN` to specific domains
- **MongoDB**: Use a secure MongoDB connection string with authentication
- **HTTPS**: Use HTTPS in production

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
