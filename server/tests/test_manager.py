import pytest
from src.db.manager import MongoDBManager
from pymongo.errors import ConnectionFailure


class TestMongoDBManager:
    """Test MongoDB manager module"""
    
    def setup_method(self):
        """Setup test method"""
        try:
            self.mongo_manager = MongoDBManager()
        except ConnectionFailure:
            # MongoDB is not running, skip all tests
            pytest.skip("MongoDB is not running locally")
    
    def test_list_databases(self):
        """Test list_databases method"""
        databases = self.mongo_manager.list_databases()
        assert isinstance(databases, list)
        # Should at least have the admin database
        assert "admin" in databases
    
    def test_create_and_drop_database(self):
        """Test create_database and drop_database methods"""
        test_db_name = "test_db"
        
        # Create database
        create_result = self.mongo_manager.create_database(test_db_name)
        assert create_result
        
        # Check if database exists
        databases = self.mongo_manager.list_databases()
        assert test_db_name in databases
        
        # Drop database
        drop_result = self.mongo_manager.drop_database(test_db_name)
        assert drop_result
        
        # Check if database is gone
        databases = self.mongo_manager.list_databases()
        assert test_db_name not in databases
    
    def test_list_collections(self):
        """Test list_collections method"""
        # Use admin database which should always exist
        collections = self.mongo_manager.list_collections("admin")
        assert isinstance(collections, list)
    
    def test_create_and_drop_collection(self):
        """Test create_collection and drop_collection methods"""
        test_db_name = "test_db"
        test_collection_name = "test_collection"
        
        try:
            # Create database
            self.mongo_manager.create_database(test_db_name)
            
            # Create collection
            create_result = self.mongo_manager.create_collection(test_db_name, test_collection_name)
            assert create_result
            
            # Check if collection exists
            collections = self.mongo_manager.list_collections(test_db_name)
            assert test_collection_name in collections
            
            # Drop collection
            drop_result = self.mongo_manager.drop_collection(test_db_name, test_collection_name)
            assert drop_result
            
            # Check if collection is gone
            collections = self.mongo_manager.list_collections(test_db_name)
            assert test_collection_name not in collections
        finally:
            # Clean up
            self.mongo_manager.drop_database(test_db_name)
