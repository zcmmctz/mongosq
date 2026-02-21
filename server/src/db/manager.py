import logging
from pymongo.errors import PyMongoError
from src.db.connection import mongo_conn

logger = logging.getLogger(__name__)


class MongoDBManager:
    """MongoDB database manager"""
    
    def __init__(self):
        """Initialize MongoDB manager"""
        # Don't store client instance, get it from mongo_conn when needed
        pass
    
    def get_client(self):
        """Get the current MongoDB client instance"""
        return mongo_conn.get_client()
    
    def list_databases(self):
        """List all databases"""
        try:
            client = self.get_client()
            databases = client.list_database_names()
            logger.info(f"Found {len(databases)} databases: {databases}")
            return databases
        except PyMongoError as e:
            logger.error(f"Error listing databases: {str(e)}")
            raise
    
    def create_database(self, db_name):
        """Create a new database"""
        try:
            client = self.get_client()
            # In MongoDB, databases are created when you first write data to them
            db = client[db_name]
            # Create a dummy collection to ensure the database is created
            db.dummy.insert_one({"created": True})
            db.dummy.drop()
            logger.info(f"Database {db_name} created successfully")
            return True
        except PyMongoError as e:
            logger.error(f"Error creating database {db_name}: {str(e)}")
            raise
    
    def drop_database(self, db_name):
        """Drop a database"""
        try:
            client = self.get_client()
            # Check if database exists
            if db_name not in client.list_database_names():
                logger.warning(f"Database {db_name} does not exist")
                return False
            
            client.drop_database(db_name)
            logger.info(f"Database {db_name} dropped successfully")
            return True
        except PyMongoError as e:
            logger.error(f"Error dropping database {db_name}: {str(e)}")
            raise
    
    def list_collections(self, db_name):
        """List all collections in a database"""
        try:
            client = self.get_client()
            db = client[db_name]
            collections = db.list_collection_names()
            logger.info(f"Found {len(collections)} collections in {db_name}: {collections}")
            return collections
        except PyMongoError as e:
            logger.error(f"Error listing collections in {db_name}: {str(e)}")
            raise
    
    def create_collection(self, db_name, collection_name):
        """Create a new collection"""
        try:
            client = self.get_client()
            db = client[db_name]
            db.create_collection(collection_name)
            logger.info(f"Collection {collection_name} created in {db_name}")
            return True
        except PyMongoError as e:
            logger.error(f"Error creating collection {collection_name} in {db_name}: {str(e)}")
            raise
    
    def drop_collection(self, db_name, collection_name):
        """Drop a collection"""
        try:
            client = self.get_client()
            db = client[db_name]
            if collection_name in db.list_collection_names():
                db.drop_collection(collection_name)
                logger.info(f"Collection {collection_name} dropped from {db_name}")
                return True
            else:
                logger.warning(f"Collection {collection_name} does not exist in {db_name}")
                return False
        except PyMongoError as e:
            logger.error(f"Error dropping collection {collection_name} from {db_name}: {str(e)}")
            raise
    
    def insert_document(self, db_name, collection_name, document):
        """Insert a single document"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            result = collection.insert_one(document)
            logger.info(f"Document inserted with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error inserting document: {str(e)}")
            raise
    
    def insert_many_documents(self, db_name, collection_name, documents):
        """Insert multiple documents"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            result = collection.insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents")
            return [str(_id) for _id in result.inserted_ids]
        except PyMongoError as e:
            logger.error(f"Error inserting multiple documents: {str(e)}")
            raise
    
    def find_documents(self, db_name, collection_name, filter=None, projection=None, sort=None, limit=100, skip=0):
        """Find documents with optional filters"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            
            query = collection.find(filter or {}, projection or {})
            
            if sort:
                query = query.sort(sort)
            
            query = query.skip(skip).limit(limit)
            
            documents = list(query)
            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            logger.info(f"Found {len(documents)} documents")
            return documents
        except PyMongoError as e:
            logger.error(f"Error finding documents: {str(e)}")
            raise
    
    def find_one_document(self, db_name, collection_name, filter=None, projection=None):
        """Find a single document"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            document = collection.find_one(filter or {}, projection or {})
            
            if document and '_id' in document:
                document['_id'] = str(document['_id'])
            
            logger.info(f"Found document: {document}")
            return document
        except PyMongoError as e:
            logger.error(f"Error finding single document: {str(e)}")
            raise
    
    def update_document(self, db_name, collection_name, filter, update, upsert=False):
        """Update a document"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            result = collection.update_one(filter, update, upsert=upsert)
            
            logger.info(f"Updated {result.modified_count} documents, upserted: {result.upserted_id}")
            return {
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None
            }
        except PyMongoError as e:
            logger.error(f"Error updating document: {str(e)}")
            raise
    
    def delete_document(self, db_name, collection_name, filter):
        """Delete a document"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            result = collection.delete_one(filter)
            
            logger.info(f"Deleted {result.deleted_count} documents")
            return result.deleted_count
        except PyMongoError as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise
    
    def delete_many_documents(self, db_name, collection_name, filter):
        """Delete multiple documents"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            result = collection.delete_many(filter)
            
            logger.info(f"Deleted {result.deleted_count} documents")
            return result.deleted_count
        except PyMongoError as e:
            logger.error(f"Error deleting multiple documents: {str(e)}")
            raise
    
    def count_documents(self, db_name, collection_name, filter=None):
        """Count documents matching a filter"""
        try:
            client = self.get_client()
            db = client[db_name]
            collection = db[collection_name]
            count = collection.count_documents(filter or {})
            
            logger.info(f"Found {count} documents matching filter")
            return count
        except PyMongoError as e:
            logger.error(f"Error counting documents: {str(e)}")
            raise


# Create global MongoDB manager instance
mongo_manager = MongoDBManager()
