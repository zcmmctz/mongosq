import { defineStore } from 'pinia';
import { apiService } from '../services/api';


export const useDatabaseStore = defineStore('database', {
  state: () => ({
    // Databases
    databases: [] as string[],
    databasesLoading: false,
    databasesError: null as string | null,
    
    // Collections
    collections: [] as string[],
    collectionsLoading: false,
    collectionsError: null as string | null,
    
    // Documents
    documents: [] as Record<string, unknown>[],
    documentsLoading: false,
    documentsError: null as string | null,
    documentCount: 0,
    
    // Database connection settings
    connectionSettings: {
      mongodb_uri: 'mongodb://localhost:27017',
      mongodb_db_name: 'admin',
      mongodb_max_pool_size: 100,
      mongodb_min_pool_size: 10,
      mongodb_max_idle_time_ms: 300000
    } as Record<string, unknown>,
    connectionSettingsLoading: false,
    connectionSettingsError: null as string | null,
    connected: false,
    
    // Current state
    currentDatabase: null as string | null,
    currentCollection: null as string | null,
    
    // General loading state
    loading: false,
    error: null as string | null
  }),

  getters: {
    databaseCount: (state) => state.databases.length,
    collectionCount: (state) => state.collections.length,
    documentCount: (state) => state.documentCount,
    isLoading: (state) => state.loading || state.databasesLoading || state.collectionsLoading || state.documentsLoading,
    hasError: (state) => !!state.error || !!state.databasesError || !!state.collectionsError || !!state.documentsError
  },

  actions: {
    /**
     * Clear all errors
     */
    clearErrors() {
      this.error = null;
      this.databasesError = null;
      this.collectionsError = null;
      this.documentsError = null;
    },

    /**
     * Fetch all databases
     */
    async fetchDatabases() {
      try {
        this.databasesLoading = true;
        this.databasesError = null;
        
        const response = await apiService.listDatabases();
        this.databases = response.databases;
        
        return response.databases;
      } catch (error) {
        this.databasesError = `Failed to fetch databases: ${String(error)}`;
        this.databases = [];
        throw error;
      } finally {
        this.databasesLoading = false;
      }
    },

    /**
     * Create a new database
     */
    async createDatabase(dbName: string) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.createDatabase(dbName);
        
        // Refresh databases list
        await this.fetchDatabases();
        
        return response;
      } catch (error) {
        this.error = `Failed to create database: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Delete a database
     */
    async deleteDatabase(dbName: string) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.deleteDatabase(dbName);
        
        // Refresh databases list
        await this.fetchDatabases();
        
        // Clear collections if current database was deleted
        if (this.currentDatabase === dbName) {
          this.collections = [];
          this.currentDatabase = null;
        }
        
        return response;
      } catch (error) {
        this.error = `Failed to delete database: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Fetch collections for a database
     */
    async fetchCollections(dbName: string) {
      try {
        this.collectionsLoading = true;
        this.collectionsError = null;
        this.currentDatabase = dbName;
        
        const response = await apiService.listCollections(dbName);
        this.collections = response.collections;
        
        return response.collections;
      } catch (error) {
        this.collectionsError = `Failed to fetch collections: ${String(error)}`;
        this.collections = [];
        throw error;
      } finally {
        this.collectionsLoading = false;
      }
    },

    /**
     * Create a new collection
     */
    async createCollection(dbName: string, collectionName: string) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.createCollection(dbName, collectionName);
        
        // Refresh collections list if current database matches
        if (this.currentDatabase === dbName) {
          await this.fetchCollections(dbName);
        }
        
        return response;
      } catch (error) {
        this.error = `Failed to create collection: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Delete a collection
     */
    async deleteCollection(dbName: string, collectionName: string) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.deleteCollection(dbName, collectionName);
        
        // Refresh collections list if current database matches
        if (this.currentDatabase === dbName) {
          await this.fetchCollections(dbName);
        }
        
        return response;
      } catch (error) {
        this.error = `Failed to delete collection: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Set current database
     */
    setCurrentDatabase(dbName: string | null) {
      this.currentDatabase = dbName;
      if (!dbName) {
        this.collections = [];
        this.currentCollection = null;
        this.documents = [];
      }
    },

    /**
     * Set current collection
     */
    setCurrentCollection(collectionName: string | null) {
      this.currentCollection = collectionName;
      if (!collectionName) {
        this.documents = [];
        this.documentCount = 0;
      }
    },

    /**
     * Fetch documents for a collection
     */
    async fetchDocuments(dbName: string, collectionName: string, filter?: Record<string, unknown>, limit: number = 100, skip: number = 0, sort?: Record<string, unknown>) {
      try {
        this.documentsLoading = true;
        this.documentsError = null;
        this.currentDatabase = dbName;
        this.currentCollection = collectionName;
        
        const response = await apiService.findDocuments(dbName, collectionName, filter, limit, skip, sort);
        this.documents = response.documents;
        this.documentCount = response.count;
        
        return response.documents;
      } catch (error) {
        this.documentsError = `Failed to fetch documents: ${String(error)}`;
        this.documents = [];
        this.documentCount = 0;
        throw error;
      } finally {
        this.documentsLoading = false;
      }
    },

    /**
     * Create a new document
     */
    async createDocument(dbName: string, collectionName: string, document: Record<string, unknown>) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.createDocument(dbName, collectionName, document);
        
        // Refresh documents list if current collection matches
        if (this.currentDatabase === dbName && this.currentCollection === collectionName) {
          await this.fetchDocuments(dbName, collectionName);
        }
        
        return response;
      } catch (error) {
        this.error = `Failed to create document: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Update a document
     */
    async updateDocument(dbName: string, collectionName: string, documentId: string, update: Record<string, unknown>, upsert: boolean = false) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.updateDocument(dbName, collectionName, documentId, update, upsert);
        
        // Refresh documents list if current collection matches
        if (this.currentDatabase === dbName && this.currentCollection === collectionName) {
          await this.fetchDocuments(dbName, collectionName);
        }
        
        return response;
      } catch (error) {
        this.error = `Failed to update document: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Delete a document
     */
    async deleteDocument(dbName: string, collectionName: string, documentId: string) {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await apiService.deleteDocument(dbName, collectionName, documentId);
        
        // Refresh documents list if current collection matches
        if (this.currentDatabase === dbName && this.currentCollection === collectionName) {
          await this.fetchDocuments(dbName, collectionName);
        }
        
        return response;
      } catch (error) {
        this.error = `Failed to delete document: ${String(error)}`;
        throw error;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Count documents in a collection
     */
    async countDocuments(dbName: string, collectionName: string, filter?: Record<string, unknown>) {
      try {
        this.documentsLoading = true;
        this.documentsError = null;
        
        const response = await apiService.countDocuments(dbName, collectionName, filter);
        this.documentCount = response.count;
        
        return response.count;
      } catch (error) {
        this.documentsError = `Failed to count documents: ${String(error)}`;
        this.documentCount = 0;
        throw error;
      } finally {
        this.documentsLoading = false;
      }
    },

    /**
     * Fetch database connection settings
     */
    async fetchConnectionSettings() {
      try {
        this.connectionSettingsLoading = true;
        this.connectionSettingsError = null;
        
        const response = await apiService.getConnectionSettings();
        this.connectionSettings = response;
        this.connected = response.connected as boolean;
        
        return response;
      } catch (error) {
        this.connectionSettingsError = `Failed to fetch connection settings: ${String(error)}`;
        throw error;
      } finally {
        this.connectionSettingsLoading = false;
      }
    },

    /**
     * Update database connection settings
     */
    async updateConnectionSettings(settings: Record<string, unknown>) {
      try {
        this.connectionSettingsLoading = true;
        this.connectionSettingsError = null;
        
        const response = await apiService.updateConnectionSettings(settings);
        
        // Refresh settings after update
        await this.fetchConnectionSettings();
        
        return response;
      } catch (error) {
        this.connectionSettingsError = `Failed to update connection settings: ${String(error)}`;
        throw error;
      } finally {
        this.connectionSettingsLoading = false;
      }
    }
  }
});
