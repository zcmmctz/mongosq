from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import jwt
from datetime import datetime, timedelta
from src.db.manager import mongo_manager
from src.db.connection import mongo_conn
from src.config.security import verify_api_key
from src.config.settings import settings


# Create FastAPI application
app = FastAPI(
    title="MongoDB Database Management API",
    description="API for managing MongoDB databases and collections",
    version="1.0.0"
)


cors_allow_origin = settings.cors_allow_origin.split(',')
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origin,  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
if os.path.exists("/app/static"):
    app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")

# Pydantic models for request validation
class DatabaseCreate(BaseModel):
    db_name: str = Field(..., min_length=1, description="Name of the database to create")

class DatabaseDelete(BaseModel):
    db_name: str = Field(..., min_length=1, description="Name of the database to delete")

class CollectionCreate(BaseModel):
    db_name: str = Field(..., min_length=1, description="Name of the database")
    collection_name: str = Field(..., min_length=1, description="Name of the collection to create")

class CollectionDelete(BaseModel):
    db_name: str = Field(..., min_length=1, description="Name of the database")
    collection_name: str = Field(..., min_length=1, description="Name of the collection to delete")

# Pydantic models for response formatting
class MessageResponse(BaseModel):
    message: str
    success: bool

class LoginRequest(BaseModel):
    account: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    message: str
    success: bool

class DatabasesResponse(BaseModel):
    databases: List[str]
    count: int

class CollectionsResponse(BaseModel):
    collections: List[str]
    count: int
    database: str

# Pydantic models for document operations
class DocumentCreate(BaseModel):
    document: dict = Field(..., description="Document to create")

class DocumentUpdate(BaseModel):
    update: dict = Field(..., description="Update operations")
    upsert: bool = Field(False, description="Whether to upsert the document")

class DocumentResponse(BaseModel):
    id: str = Field(..., description="Document ID")
    document: dict = Field(..., description="Document data")

class DocumentsResponse(BaseModel):
    documents: List[dict]
    count: int
    database: str
    collection: str

class DocumentCountResponse(BaseModel):
    count: int
    database: str
    collection: str

class DocumentDeleteResponse(BaseModel):
    deleted_count: int
    message: str

class DocumentUpdateResponse(BaseModel):
    modified_count: int
    upserted_id: Optional[str]
    message: str

# Pydantic model for database connection settings
class DatabaseConnectionSettings(BaseModel):
    mongodb_uri: str = Field(..., description="MongoDB connection URI")
    mongodb_db_name: str = Field(default="admin", description="MongoDB database name")
    mongodb_max_pool_size: int = Field(default=100, description="Maximum connection pool size")
    mongodb_min_pool_size: int = Field(default=10, description="Minimum connection pool size")
    mongodb_max_idle_time_ms: int = Field(default=300000, description="Maximum idle time in milliseconds")

# Login endpoint
@app.post("/api/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Login with account and password"""
    try:
        # Get account and password from settings
        account = settings.account
        password = settings.password
        
        # Verify account and password
        if login_data.account != account or login_data.password != password:
            raise HTTPException(status_code=401, detail="Invalid account or password")
        
        # Generate JWT token
        api_key = settings.api_key
        payload = {
            "sub": account,
            "exp": datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
        }
        token = jwt.encode(payload, api_key, algorithm="HS256")
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            message="Login successful",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")

# Health check endpoint
@app.get("/api/health", response_model=MessageResponse)
async def health_check():
    """Check if the API is running and MongoDB is connected"""
    try:
        if not mongo_conn.connected:
            mongo_conn.connect()
        return MessageResponse(message="API is healthy and MongoDB is connected", success=True)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

# Database endpoints
@app.get("/api/databases", response_model=DatabasesResponse)
async def list_databases():
    """List all databases"""
    try:
        databases = mongo_manager.list_databases()
        return DatabasesResponse(databases=databases, count=len(databases))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing databases: {str(e)}")

@app.post("/api/databases", response_model=MessageResponse, dependencies=[Depends(verify_api_key)])
async def create_database(db: DatabaseCreate):
    """Create a new database"""
    try:
        result = mongo_manager.create_database(db.db_name)
        if result:
            return MessageResponse(message=f"Database {db.db_name} created successfully", success=True)
        else:
            raise HTTPException(status_code=400, detail=f"Failed to create database {db.db_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating database: {str(e)}")

@app.delete("/api/databases/{db_name}", response_model=MessageResponse, dependencies=[Depends(verify_api_key)])
async def delete_database(db_name: str):
    """Delete a database"""
    try:
        result = mongo_manager.drop_database(db_name)
        if result:
            return MessageResponse(message=f"Database {db_name} deleted successfully", success=True)
        else:
            raise HTTPException(status_code=404, detail=f"Database {db_name} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting database: {str(e)}")

# Collection endpoints
@app.get("/api/databases/{db_name}/collections", response_model=CollectionsResponse)
async def list_collections(db_name: str):
    """List all collections in a database"""
    try:
        collections = mongo_manager.list_collections(db_name)
        return CollectionsResponse(
            collections=collections,
            count=len(collections),
            database=db_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing collections: {str(e)}")

@app.post("/api/collections", response_model=MessageResponse, dependencies=[Depends(verify_api_key)])
async def create_collection(collection: CollectionCreate):
    """Create a new collection"""
    try:
        result = mongo_manager.create_collection(collection.db_name, collection.collection_name)
        if result:
            return MessageResponse(
                message=f"Collection {collection.collection_name} created in {collection.db_name}",
                success=True
            )
        else:
            raise HTTPException(status_code=400, detail=f"Failed to create collection")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating collection: {str(e)}")

@app.delete("/api/databases/{db_name}/collections/{collection_name}", response_model=MessageResponse, dependencies=[Depends(verify_api_key)])
async def delete_collection(db_name: str, collection_name: str):
    """Delete a collection"""
    try:
        result = mongo_manager.drop_collection(db_name, collection_name)
        if result:
            return MessageResponse(
                message=f"Collection {collection_name} deleted from {db_name}",
                success=True
            )
        else:
            raise HTTPException(status_code=404, detail=f"Collection {collection_name} not found in {db_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting collection: {str(e)}")

# Document endpoints
@app.post("/api/databases/{db_name}/collections/{collection_name}/documents", response_model=MessageResponse, dependencies=[Depends(verify_api_key)])
async def create_document(db_name: str, collection_name: str, doc: DocumentCreate):
    """Create a new document"""
    try:
        document_id = mongo_manager.insert_document(db_name, collection_name, doc.document)
        return MessageResponse(
            message=f"Document created with ID: {document_id}",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating document: {str(e)}")

@app.get("/api/databases/{db_name}/collections/{collection_name}/documents", response_model=DocumentsResponse)
async def find_documents(
    db_name: str, 
    collection_name: str, 
    filter: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    sort: Optional[str] = None
):
    """Find documents with optional filters"""
    try:
        # Parse filter if provided
        filter_dict = {}
        if filter:
            import json
            try:
                filter_dict = json.loads(filter)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid filter format")
        
        # Parse sort if provided
        sort_tuple = None
        if sort:
            import json
            try:
                sort_dict = json.loads(sort)
                sort_tuple = [(k, v) for k, v in sort_dict.items()]
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid sort format")
        
        documents = mongo_manager.find_documents(
            db_name, 
            collection_name, 
            filter=filter_dict,
            sort=sort_tuple,
            limit=limit,
            skip=skip
        )
        
        return DocumentsResponse(
            documents=documents,
            count=len(documents),
            database=db_name,
            collection=collection_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding documents: {str(e)}")

@app.get("/api/databases/{db_name}/collections/{collection_name}/documents/{document_id}", response_model=DocumentResponse)
async def find_document(db_name: str, collection_name: str, document_id: str):
    """Find a document by ID"""
    try:
        from bson.objectid import ObjectId
        try:
            doc_id = ObjectId(document_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid document ID format")
        
        document = mongo_manager.find_one_document(
            db_name, 
            collection_name, 
            filter={"_id": doc_id}
        )
        
        if not document:
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        return DocumentResponse(
            id=document_id,
            document=document
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding document: {str(e)}")

@app.put("/api/databases/{db_name}/collections/{collection_name}/documents/{document_id}", response_model=DocumentUpdateResponse, dependencies=[Depends(verify_api_key)])
async def update_document(db_name: str, collection_name: str, document_id: str, update_data: DocumentUpdate):
    """Update a document"""
    try:
        from bson.objectid import ObjectId
        try:
            doc_id = ObjectId(document_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid document ID format")
        
        result = mongo_manager.update_document(
            db_name, 
            collection_name, 
            filter={"_id": doc_id},
            update=update_data.update,
            upsert=update_data.upsert
        )
        
        return DocumentUpdateResponse(
            modified_count=result["modified_count"],
            upserted_id=result["upserted_id"],
            message=f"Document {document_id} updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating document: {str(e)}")

@app.delete("/api/databases/{db_name}/collections/{collection_name}/documents/{document_id}", response_model=DocumentDeleteResponse, dependencies=[Depends(verify_api_key)])
async def delete_document(db_name: str, collection_name: str, document_id: str):
    """Delete a document"""
    try:
        from bson.objectid import ObjectId
        try:
            doc_id = ObjectId(document_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid document ID format")
        
        deleted_count = mongo_manager.delete_document(
            db_name, 
            collection_name, 
            filter={"_id": doc_id}
        )
        
        return DocumentDeleteResponse(
            deleted_count=deleted_count,
            message=f"Document {document_id} deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@app.get("/api/databases/{db_name}/collections/{collection_name}/documents/count", response_model=DocumentCountResponse)
async def count_documents(db_name: str, collection_name: str, filter: Optional[str] = None):
    """Count documents matching a filter"""
    try:
        # Parse filter if provided
        filter_dict = {}
        if filter:
            import json
            try:
                filter_dict = json.loads(filter)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid filter format")
        
        count = mongo_manager.count_documents(
            db_name, 
            collection_name, 
            filter=filter_dict
        )
        
        return DocumentCountResponse(
            count=count,
            database=db_name,
            collection=collection_name
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting documents: {str(e)}")

# Database connection settings endpoint
@app.post("/api/settings/connection", response_model=MessageResponse, dependencies=[Depends(verify_api_key)])
async def update_connection_settings(settings_data: DatabaseConnectionSettings):
    """Update MongoDB connection settings"""
    try:
        # Update connection settings
        mongo_conn.update_connection_settings(
            uri=settings_data.mongodb_uri,
            db_name=settings_data.mongodb_db_name,
            max_pool_size=settings_data.mongodb_max_pool_size,
            min_pool_size=settings_data.mongodb_min_pool_size,
            max_idle_time_ms=settings_data.mongodb_max_idle_time_ms
        )
        
        return MessageResponse(
            message="Database connection settings updated successfully",
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating connection settings: {str(e)}")

@app.get("/api/settings/connection", response_model=dict)
async def get_connection_settings():
    """Get current MongoDB connection settings"""
    try:
        return {
            "mongodb_uri": mongo_conn.mongodb_uri,
            "mongodb_db_name": mongo_conn.mongodb_db_name,
            "mongodb_max_pool_size": mongo_conn.mongodb_max_pool_size,
            "mongodb_min_pool_size": mongo_conn.mongodb_min_pool_size,
            "mongodb_max_idle_time_ms": mongo_conn.mongodb_max_idle_time_ms,
            "connected": mongo_conn.connected
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting connection settings: {str(e)}")

# API root endpoint (moved to /api to avoid conflict with static files)
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "MongoDB Database Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=22222,
        reload=True
    )
