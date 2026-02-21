import axios, { type AxiosInstance, type AxiosError } from 'axios';

// API response types
interface MessageResponse {
  message: string;
  success: boolean;
}

interface DatabasesResponse {
  databases: string[];
  count: number;
}

interface CollectionsResponse {
  collections: string[];
  count: number;
  database: string;
}

interface DocumentResponse {
  _id: string;
  document: Record<string, unknown>;
}

interface DocumentsResponse {
  documents: Record<string, unknown>[];
  count: number;
  database: string;
  collection: string;
}

interface DocumentCountResponse {
  count: number;
  database: string;
  collection: string;
}

interface DocumentDeleteResponse {
  deleted_count: number;
  message: string;
}

interface DocumentUpdateResponse {
  modified_count: number;
  upserted_id: string | null;
  message: string;
}

// Request types
interface DatabaseCreate {
  db_name: string;
}

interface CollectionCreate {
  db_name: string;
  collection_name: string;
}

interface DocumentCreate {
  document: Record<string, unknown>;
}

interface DocumentUpdate {
  update: Record<string, unknown>;
  upsert: boolean;
}

interface LoginRequest {
  account: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  message: string;
  success: boolean;
}

class ApiService {
  private axios: AxiosInstance;
  private apiKey: string | null = null;

  constructor() {
    // Create axios instance with base URL (relative path for Docker deployment)
    this.axios = axios.create({
      baseURL: '', // Use relative path to avoid CORS issues in Docker
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Load API key from localStorage
    this.apiKey = localStorage.getItem('apiKey');
  }

  /**
   * Set API key for authenticated requests
   */
  setApiKey(key: string): void {
    this.apiKey = key;
    localStorage.setItem('apiKey', key);
  }

  /**
   * Remove API key
   */
  removeApiKey(): void {
    this.apiKey = null;
    localStorage.removeItem('apiKey');
  }

  /**
   * Get API key
   */
  getApiKey(): string | null {
    return this.apiKey;
  }

  /**
   * Login with account and password
   */
  async login(account: string, password: string): Promise<LoginResponse> {
    try {
      const response = await this.axios.post<LoginResponse>('/api/login', {
        account,
        password
      });
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Add authorization header to request config
   */
  private getAuthConfig() {
    if (this.apiKey) {
      return {
        headers: {
          Authorization: `Bearer ${this.apiKey}`
        }
      };
    }
    return {};
  }

  /**
   * Handle API errors
   */
  private handleError(error: unknown): never {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      if (axiosError.response) {
        // Server responded with error status
        const message = axiosError.response.data as { detail?: string };
        throw new Error(message.detail || `API error: ${axiosError.response.status}`);
      } else if (axiosError.request) {
        // Request was made but no response
        throw new Error('No response from server. Please check if the backend is running.');
      } else {
        // Request setup error
        throw new Error(`Request error: ${axiosError.message}`);
      }
    }
    throw new Error(`Unknown error: ${String(error)}`);
  }

  // Health check
  async healthCheck(): Promise<MessageResponse> {
    try {
      const response = await this.axios.get<MessageResponse>('/api/health');
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  // Database operations
  async listDatabases(): Promise<DatabasesResponse> {
    try {
      const response = await this.axios.get<DatabasesResponse>('/api/databases');
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async createDatabase(db_name: string): Promise<MessageResponse> {
    try {
      const response = await this.axios.post<MessageResponse>(
        '/api/databases',
        { db_name },
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async deleteDatabase(db_name: string): Promise<MessageResponse> {
    try {
      const response = await this.axios.delete<MessageResponse>(
        `/api/databases/${db_name}`,
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  // Collection operations
  async listCollections(db_name: string): Promise<CollectionsResponse> {
    try {
      const response = await this.axios.get<CollectionsResponse>(
        `/api/databases/${db_name}/collections`
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async createCollection(db_name: string, collection_name: string): Promise<MessageResponse> {
    try {
      const response = await this.axios.post<MessageResponse>(
        '/api/collections',
        { db_name, collection_name },
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async deleteCollection(db_name: string, collection_name: string): Promise<MessageResponse> {
    try {
      const response = await this.axios.delete<MessageResponse>(
        `/api/databases/${db_name}/collections/${collection_name}`,
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  // Document operations
  async createDocument(db_name: string, collection_name: string, document: Record<string, unknown>): Promise<MessageResponse> {
    try {
      const response = await this.axios.post<MessageResponse>(
        `/api/databases/${db_name}/collections/${collection_name}/documents`,
        { document },
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async findDocuments(
    db_name: string, 
    collection_name: string, 
    filter?: Record<string, unknown>,
    limit: number = 100,
    skip: number = 0,
    sort?: Record<string, unknown>
  ): Promise<DocumentsResponse> {
    try {
      const params: Record<string, unknown> = { limit, skip };
      if (filter) {
        params.filter = JSON.stringify(filter);
      }
      if (sort) {
        params.sort = JSON.stringify(sort);
      }
      
      const response = await this.axios.get<DocumentsResponse>(
        `/api/databases/${db_name}/collections/${collection_name}/documents`,
        { params }
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async findDocument(db_name: string, collection_name: string, document_id: string): Promise<DocumentResponse> {
    try {
      const response = await this.axios.get<DocumentResponse>(
        `/api/databases/${db_name}/collections/${collection_name}/documents/${document_id}`
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async updateDocument(
    db_name: string, 
    collection_name: string, 
    document_id: string, 
    update: Record<string, unknown>,
    upsert: boolean = false
  ): Promise<DocumentUpdateResponse> {
    try {
      const response = await this.axios.put<DocumentUpdateResponse>(
        `/api/databases/${db_name}/collections/${collection_name}/documents/${document_id}`,
        { update, upsert },
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async deleteDocument(db_name: string, collection_name: string, document_id: string): Promise<DocumentDeleteResponse> {
    try {
      const response = await this.axios.delete<DocumentDeleteResponse>(
        `/api/databases/${db_name}/collections/${collection_name}/documents/${document_id}`,
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async countDocuments(
    db_name: string, 
    collection_name: string, 
    filter?: Record<string, unknown>
  ): Promise<DocumentCountResponse> {
    try {
      const params: Record<string, unknown> = {};
      if (filter) {
        params.filter = JSON.stringify(filter);
      }
      
      const response = await this.axios.get<DocumentCountResponse>(
        `/api/databases/${db_name}/collections/${collection_name}/documents/count`,
        { params }
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  // Database connection settings operations
  async getConnectionSettings(): Promise<Record<string, unknown>> {
    try {
      const response = await this.axios.get<Record<string, unknown>>('/api/settings/connection');
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async updateConnectionSettings(settings: Record<string, unknown>): Promise<MessageResponse> {
    try {
      const response = await this.axios.post<MessageResponse>(
        '/api/settings/connection',
        settings,
        this.getAuthConfig()
      );
      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }
}

// Create singleton instance
export const apiService = new ApiService();

// Export types
export type {
  MessageResponse,
  DatabasesResponse,
  CollectionsResponse,
  DocumentResponse,
  DocumentsResponse,
  DocumentCountResponse,
  DocumentDeleteResponse,
  DocumentUpdateResponse,
  DatabaseCreate,
  CollectionCreate,
  DocumentCreate,
  DocumentUpdate,
  LoginRequest,
  LoginResponse
};
