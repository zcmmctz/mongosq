import pytest
from src.db.connection import MongoDBConnection
from pymongo.errors import ConnectionFailure


class TestMongoDBConnection:
    """Test MongoDB connection module"""
    
    def setup_method(self):
        """Setup test method"""
        self.mongo_conn = MongoDBConnection()
    
    def teardown_method(self):
        """Teardown test method"""
        if self.mongo_conn.connected:
            self.mongo_conn.disconnect()
    
    def test_initialization(self):
        """Test initialization"""
        assert not self.mongo_conn.connected
        assert self.mongo_conn.client is None
        assert self.mongo_conn.db is None
    
    def test_connect(self):
        """Test connect method"""
        # This test will fail if MongoDB is not running locally
        # For CI/CD, we should use a mock or test MongoDB instance
        try:
            self.mongo_conn.connect()
            assert self.mongo_conn.connected
            assert self.mongo_conn.client is not None
            assert self.mongo_conn.db is not None
        except ConnectionFailure:
            # MongoDB is not running, skip this test
            pytest.skip("MongoDB is not running locally")
    
    def test_disconnect(self):
        """Test disconnect method"""
        try:
            self.mongo_conn.connect()
            assert self.mongo_conn.connected
            self.mongo_conn.disconnect()
            assert not self.mongo_conn.connected
        except ConnectionFailure:
            # MongoDB is not running, skip this test
            pytest.skip("MongoDB is not running locally")
    
    def test_get_client(self):
        """Test get_client method"""
        try:
            client = self.mongo_conn.get_client()
            assert self.mongo_conn.connected
            assert client is not None
        except ConnectionFailure:
            # MongoDB is not running, skip this test
            pytest.skip("MongoDB is not running locally")
    
    def test_get_db(self):
        """Test get_db method"""
        try:
            db = self.mongo_conn.get_db()
            assert self.mongo_conn.connected
            assert db is not None
        except ConnectionFailure:
            # MongoDB is not running, skip this test
            pytest.skip("MongoDB is not running locally")
