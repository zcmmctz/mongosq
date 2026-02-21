<template>
  <q-page class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <!-- Page header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Document Management</h1>
          <p class="text-gray-600">Manage documents in your MongoDB collections</p>
        </div>
        
        <q-btn 
          label="Create Document" 
          color="primary" 
          icon="add" 
          @click="showCreateForm = true"
          :disabled="!authStore.isAuthenticated || !selectedDatabase || !selectedCollection"
        />
      </div>

      <!-- Database and Collection selection -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- Database selection -->
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="font-medium mb-4">Select Database</h3>
          <q-select
            v-model="selectedDatabase"
            :options="databaseStore.databases"
            label="Database"
            placeholder="Choose a database"
            clearable
            :loading="databaseStore.databasesLoading"
            @update:model-value="onDatabaseChange"
          />
        </div>

        <!-- Collection selection -->
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="font-medium mb-4">Select Collection</h3>
          <q-select
            v-model="selectedCollection"
            :options="databaseStore.collections"
            label="Collection"
            placeholder="Choose a collection"
            clearable
            :loading="databaseStore.collectionsLoading"
            :disable="!selectedDatabase"
            @update:model-value="onCollectionChange"
          />
        </div>
      </div>

      <!-- Authentication warning -->
      <div v-if="!authStore.isAuthenticated" class="bg-warning/20 border border-warning rounded-lg p-4 mb-6">
        <div class="flex items-center gap-3">
          <q-icon name="warning" color="warning" />
          <div>
            <h3 class="font-medium text-warning">Authentication Required</h3>
            <p class="text-sm text-gray-700">
              You need to set an API key in settings to create, update, or delete documents
            </p>
            <q-btn 
              to="/settings" 
              label="Go to Settings" 
              size="sm" 
              color="warning" 
              class="mt-2"
            />
          </div>
        </div>
      </div>

      <!-- Error message -->
      <div v-if="databaseStore.documentsError" class="bg-danger/20 border border-danger rounded-lg p-4 mb-6">
        <div class="flex items-center gap-3">
          <q-icon name="error" color="danger" />
          <div>
            <h3 class="font-medium text-danger">Error</h3>
            <p class="text-sm text-gray-700">{{ databaseStore.documentsError }}</p>
            <q-btn 
              label="Retry" 
              size="sm" 
              color="danger" 
              @click="fetchDocuments" 
              class="mt-2"
            />
          </div>
        </div>
      </div>

      <!-- Document count -->
      <div v-if="selectedDatabase && selectedCollection" class="bg-white rounded-lg shadow p-4 mb-6">
        <div class="flex justify-between items-center">
          <h3 class="font-medium">Document Count</h3>
          <div class="text-lg font-semibold text-primary">{{ databaseStore.documentCount }} documents</div>
        </div>
      </div>

      <!-- Create document form -->
      <q-dialog v-model="showCreateForm" persistent>
        <q-card class="w-full max-w-2xl">
          <q-card-section>
            <h2 class="text-xl font-bold">Create New Document</h2>
          </q-card-section>
          
          <q-card-section>
            <q-form @submit="createDocument">
              <q-input
                v-model="newDocumentJSON"
                label="Document JSON"
                placeholder="{'key': 'value'}"
                type="textarea"
                rows="6"
                :rules="[val => !!val || 'Document JSON is required', val => { try { JSON.parse(val); return true; } catch { return 'Invalid JSON format' } }]"
                autofocus
              />
              
              <div class="flex justify-end gap-2 mt-4">
                <q-btn label="Cancel" @click="showCreateForm = false" />
                <q-btn label="Create" color="primary" type="submit" :loading="databaseStore.loading" />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Edit document form -->
      <q-dialog v-model="showEditForm" persistent>
        <q-card class="w-full max-w-2xl">
          <q-card-section>
            <h2 class="text-xl font-bold">Edit Document</h2>
          </q-card-section>
          
          <q-card-section>
            <q-form @submit="updateDocument">
              <q-input
                v-model="editDocumentJSON"
                label="Document JSON"
                placeholder="{'key': 'value'}"
                type="textarea"
                rows="6"
                :rules="[val => !!val || 'Document JSON is required', val => { try { JSON.parse(val); return true; } catch { return 'Invalid JSON format' } }]"
                autofocus
              />
              
              <div class="flex justify-end gap-2 mt-4">
                <q-btn label="Cancel" @click="showEditForm = false" />
                <q-btn label="Update" color="primary" type="submit" :loading="databaseStore.loading" />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Delete confirmation dialog -->
      <q-dialog v-model="showDeleteDialog" persistent>
        <q-card class="w-full max-w-md">
          <q-card-section>
            <h2 class="text-xl font-bold">Delete Document</h2>
          </q-card-section>
          
          <q-card-section>
            <p>Are you sure you want to delete this document? This action cannot be undone.</p>
          </q-card-section>
          
          <q-card-actions align="right" class="gap-2">
            <q-btn label="Cancel" @click="showDeleteDialog = false" />
            <q-btn label="Delete" color="danger" @click="deleteDocument" :loading="databaseStore.loading" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Documents table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="p-4 border-b">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <h3 class="font-semibold">
              Documents
              <span v-if="selectedDatabase && selectedCollection" class="text-gray-500 text-sm font-normal ml-2">
                in {{ selectedDatabase }}/{{ selectedCollection }}
              </span>
            </h3>
            <div class="w-full md:w-64">
              <q-input
                v-model="filterQuery"
                label="Filter"
                placeholder="Enter filter JSON"
                @keyup.enter="applyFilter"
              >
                <template #append>
                  <q-btn icon="search" @click="applyFilter" />
                </template>
              </q-input>
            </div>
          </div>
        </div>
        
        <div v-if="!selectedDatabase || !selectedCollection" class="p-12 flex flex-col items-center justify-center text-gray-500">
          <q-icon name="description" size="64px" class="mb-4" />
          <p>Please select both a database and collection to view documents</p>
        </div>
        
        <div v-else-if="databaseStore.documentsLoading" class="p-12 flex justify-center items-center">
          <q-spinner size="48px" color="primary" />
        </div>
        
        <div v-else-if="databaseStore.documents.length === 0" class="p-12 flex flex-col items-center justify-center text-gray-500">
          <q-icon name="inbox" size="64px" class="mb-4" />
          <p>No documents found in {{ selectedCollection }}</p>
          <q-btn 
            label="Create First Document" 
            color="primary" 
            @click="showCreateForm = true"
            :disabled="!authStore.isAuthenticated"
            class="mt-4"
          />
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-100">
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">_id</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Document</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(document, index) in databaseStore.documents" :key="index">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ document._id }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-sm text-gray-500 font-mono break-all">{{ JSON.stringify(document, null, 2) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button 
                      @click="editDocument(document)"
                      :disabled="!authStore.isAuthenticated"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      :class="{ 'opacity-50 cursor-not-allowed': !authStore.isAuthenticated }"
                    >
                      <span>Edit</span>
                    </button>
                    <button 
                      @click="confirmDelete(String(document._id))"
                      :disabled="!authStore.isAuthenticated"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                      :class="{ 'opacity-50 cursor-not-allowed': !authStore.isAuthenticated }"
                    >
                      <span>Delete</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useDatabaseStore } from '../stores/database';
import { useAuthStore } from '../stores/auth';
import { notificationService } from '../services/notification';

const route = useRoute();
const databaseStore = useDatabaseStore();
const authStore = useAuthStore();

// State
const selectedDatabase = ref<string | null>(null);
const selectedCollection = ref<string | null>(null);
const showCreateForm = ref(false);
const newDocumentJSON = ref('');
const showEditForm = ref(false);
const editDocumentJSON = ref('');
const documentToEdit = ref<Record<string, unknown> | null>(null);
const showDeleteDialog = ref(false);
const documentToDelete = ref('');
const filterQuery = ref('');

// Fetch databases on mount
onMounted(async () => {
  await databaseStore.fetchDatabases();
  
  // Check if database and collection are passed from route params
  const dbParam = route.query.db as string;
  const collParam = route.query.coll as string;
  
  if (dbParam) {
    selectedDatabase.value = dbParam;
    await databaseStore.fetchCollections(dbParam);
    
    if (collParam) {
      selectedCollection.value = collParam;
      await databaseStore.fetchDocuments(dbParam, collParam);
    }
  }
});

// Watch for route changes
watch(() => [route.query.db, route.query.coll], async ([newDb, newColl]) => {
  if (newDb) {
    selectedDatabase.value = newDb as string;
    await databaseStore.fetchCollections(newDb as string);
    
    if (newColl) {
      selectedCollection.value = newColl as string;
      await databaseStore.fetchDocuments(newDb as string, newColl as string);
    }
  }
}, { deep: true });

// Handle database change
async function onDatabaseChange(database: string | null) {
  if (database) {
    await databaseStore.fetchCollections(database);
    selectedCollection.value = null;
  } else {
    databaseStore.setCurrentDatabase(null);
    selectedCollection.value = null;
  }
}

// Handle collection change
async function onCollectionChange(collection: string | null) {
  if (collection && selectedDatabase.value) {
    await databaseStore.fetchDocuments(selectedDatabase.value, collection);
  } else {
    databaseStore.setCurrentCollection(null);
  }
}

// Fetch documents
async function fetchDocuments() {
  if (selectedDatabase.value && selectedCollection.value) {
    await databaseStore.fetchDocuments(selectedDatabase.value, selectedCollection.value);
  }
}

// Apply filter
async function applyFilter() {
  if (selectedDatabase.value && selectedCollection.value) {
    try {
      const filter = filterQuery.value ? JSON.parse(filterQuery.value) : {};
      await databaseStore.fetchDocuments(selectedDatabase.value, selectedCollection.value, filter);
    } catch {
      notificationService.error('Invalid filter format');
    }
  }
}

// Create document
async function createDocument() {
  if (!newDocumentJSON.value || !selectedDatabase.value || !selectedCollection.value) return;
  
  try {
    const document = JSON.parse(newDocumentJSON.value);
    await databaseStore.createDocument(selectedDatabase.value, selectedCollection.value, document);
    showCreateForm.value = false;
    newDocumentJSON.value = '';
    notificationService.success('Document created successfully');
  } catch (error) {
    console.error('Error creating document:', error);
    notificationService.error(`Failed to create document: ${String(error)}`);
  }
}

// Edit document
function editDocument(document: Record<string, unknown>) {
  documentToEdit.value = { ...document };
  // Remove _id from editable JSON since it's immutable
  const documentWithoutId = { ...document };
  delete documentWithoutId._id;
  editDocumentJSON.value = JSON.stringify(documentWithoutId, null, 2);
  showEditForm.value = true;
}

// Update document
async function updateDocument() {
  if (!editDocumentJSON.value || !selectedDatabase.value || !selectedCollection.value || !documentToEdit.value) return;
  
  try {
    const updatedDocument = JSON.parse(editDocumentJSON.value);
    // Create update operation using $set
    const update = { $set: updatedDocument };
    await databaseStore.updateDocument(selectedDatabase.value, selectedCollection.value, String(documentToEdit.value._id), update);
    showEditForm.value = false;
    editDocumentJSON.value = '';
    documentToEdit.value = null;
    notificationService.success('Document updated successfully');
  } catch (error) {
    console.error('Error updating document:', error);
    notificationService.error(`Failed to update document: ${String(error)}`);
  }
}

// Confirm delete
function confirmDelete(documentId: string) {
  documentToDelete.value = documentId;
  showDeleteDialog.value = true;
}

// Delete document
async function deleteDocument() {
  if (!documentToDelete.value || !selectedDatabase.value || !selectedCollection.value) return;
  
  try {
    await databaseStore.deleteDocument(selectedDatabase.value, selectedCollection.value, documentToDelete.value);
    showDeleteDialog.value = false;
    documentToDelete.value = '';
    notificationService.success('Document deleted successfully');
  } catch (error) {
    console.error('Error deleting document:', error);
    notificationService.error(`Failed to delete document: ${String(error)}`);
  }
}
</script>

<style scoped>
/* Add custom styles here */
</style>