import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from src.config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MongoDBConnection:
    """MongoDB connection manager with connection pool"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.client = None
        self.db = None
        self._connected = False
        # Use default settings initially
        self.mongodb_uri = settings.mongodb_uri
        self.mongodb_db_name = settings.mongodb_db_name
        self.mongodb_max_pool_size = settings.mongodb_max_pool_size
        self.mongodb_min_pool_size = settings.mongodb_min_pool_size
        self.mongodb_max_idle_time_ms = settings.mongodb_max_idle_time_ms
    
    def connect(self, uri=None, db_name=None, max_pool_size=None, min_pool_size=None, max_idle_time_ms=None):
        """Establish MongoDB connection"""
        try:
            # Use provided settings or defaults
            conn_uri = uri or self.mongodb_uri
            conn_db_name = db_name or self.mongodb_db_name
            conn_max_pool_size = max_pool_size or self.mongodb_max_pool_size
            conn_min_pool_size = min_pool_size or self.mongodb_min_pool_size
            conn_max_idle_time_ms = max_idle_time_ms or self.mongodb_max_idle_time_ms
            
            # Update instance settings
            self.mongodb_uri = conn_uri
            self.mongodb_db_name = conn_db_name
            self.mongodb_max_pool_size = conn_max_pool_size
            self.mongodb_min_pool_size = conn_min_pool_size
            self.mongodb_max_idle_time_ms = conn_max_idle_time_ms
            
            # Close existing connection if any
            if self.client:
                self.disconnect()
            
            # Create MongoClient with connection pool settings
            self.client = MongoClient(
                conn_uri,
                maxPoolSize=conn_max_pool_size,
                minPoolSize=conn_min_pool_size,
                maxIdleTimeMS=conn_max_idle_time_ms
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client[conn_db_name]
            self._connected = True
            
            logger.info(f"Successfully connected to MongoDB at {conn_uri}")
            logger.info(f"Using database: {conn_db_name}")
            
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            raise
        except PyMongoError as e:
            logger.error(f"MongoDB error: {str(e)}")
            raise
    
    def update_connection_settings(self, uri, db_name=None, max_pool_size=None, min_pool_size=None, max_idle_time_ms=None):
        """Update connection settings and reconnect"""
        try:
            # Connect with new settings
            self.connect(uri, db_name, max_pool_size, min_pool_size, max_idle_time_ms)
            return True
        except Exception as e:
            logger.error(f"Error updating connection settings: {str(e)}")
            raise
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            try:
                self.client.close()
                self._connected = False
                logger.info("MongoDB connection closed")
            except PyMongoError as e:
                logger.error(f"Error closing MongoDB connection: {str(e)}")
    
    def get_client(self):
        """Get MongoDB client instance"""
        if not self._connected:
            self.connect()
        return self.client
    
    def get_db(self):
        """Get MongoDB database instance"""
        if not self._connected:
            self.connect()
        return self.db
    
    @property
    def connected(self):
        """Check if connected to MongoDB"""
        return self._connected


# Create global MongoDB connection instance
mongo_conn = MongoDBConnection()
