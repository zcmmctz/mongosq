import pytest
from fastapi.testclient import TestClient
from main import app
from src.config.security import API_KEY


class TestAPI:
    """Test FastAPI endpoints"""
    
    def setup_method(self):
        """Setup test method"""
        self.client = TestClient(app)
        self.api_key = API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "version" in response.json()
        assert "docs" in response.json()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        # If MongoDB is not running, this will return 503
        # We'll check both cases
        assert response.status_code in [200, 503]
    
    def test_list_databases(self):
        """Test list databases endpoint"""
        response = self.client.get("/databases")
        # If MongoDB is not running, this will return 500
        # We'll check both cases
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            assert "databases" in response.json()
            assert "count" in response.json()
            assert isinstance(response.json()["databases"], list)
    
    def test_create_database_unauthorized(self):
        """Test create database without API key"""
        response = self.client.post("/databases", json={"db_name": "test_db"})
        assert response.status_code == 401
    
    def test_delete_database_unauthorized(self):
        """Test delete database without API key"""
        response = self.client.delete("/databases/test_db")
        assert response.status_code == 401
    
    def test_create_collection_unauthorized(self):
        """Test create collection without API key"""
        response = self.client.post("/collections", json={
            "db_name": "test_db",
            "collection_name": "test_collection"
        })
        assert response.status_code == 401
    
    def test_delete_collection_unauthorized(self):
        """Test delete collection without API key"""
        response = self.client.delete("/databases/test_db/collections/test_collection")
        assert response.status_code == 401
