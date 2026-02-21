<template>
  <q-page class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <!-- Page header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Collection Management</h1>
          <p class="text-gray-600">Manage collections in your MongoDB databases</p>
        </div>
        
        <q-btn 
          label="Create Collection" 
          color="primary" 
          icon="add" 
          @click="showCreateForm = true"
          :disabled="!authStore.isAuthenticated || !selectedDatabase"
        />
      </div>

      <!-- Database selection -->
      <div class="bg-white rounded-lg shadow p-4 mb-6">
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

      <!-- Authentication warning -->
      <div v-if="!authStore.isAuthenticated" class="bg-warning/20 border border-warning rounded-lg p-4 mb-6">
        <div class="flex items-center gap-3">
          <q-icon name="warning" color="warning" />
          <div>
            <h3 class="font-medium text-warning">Authentication Required</h3>
            <p class="text-sm text-gray-700">
              You need to set an API key in settings to create or delete collections
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
      <div v-if="databaseStore.collectionsError" class="bg-danger/20 border border-danger rounded-lg p-4 mb-6">
        <div class="flex items-center gap-3">
          <q-icon name="error" color="danger" />
          <div>
            <h3 class="font-medium text-danger">Error</h3>
            <p class="text-sm text-gray-700">{{ databaseStore.collectionsError }}</p>
            <q-btn 
              label="Retry" 
              size="sm" 
              color="danger" 
              @click="fetchCollections" 
              class="mt-2"
            />
          </div>
        </div>
      </div>

      <!-- Create collection form -->
      <q-dialog v-model="showCreateForm" persistent>
        <q-card class="w-full max-w-md">
          <q-card-section>
            <h2 class="text-xl font-bold">Create New Collection</h2>
          </q-card-section>
          
          <q-card-section>
            <q-form @submit="createCollection">
              <q-input
                v-model="newCollectionName"
                label="Collection Name"
                placeholder="Enter collection name"
                :rules="[val => !!val || 'Collection name is required']"
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

      <!-- Delete confirmation dialog -->
      <q-dialog v-model="showDeleteDialog" persistent>
        <q-card class="w-full max-w-md">
          <q-card-section>
            <h2 class="text-xl font-bold">Delete Collection</h2>
          </q-card-section>
          
          <q-card-section>
            <p>Are you sure you want to delete the collection <strong>{{ collectionToDelete }}</strong> from database <strong>{{ selectedDatabase }}</strong>? This action cannot be undone.</p>
          </q-card-section>
          
          <q-card-actions align="right" class="gap-2">
            <q-btn label="Cancel" @click="showDeleteDialog = false" />
            <q-btn label="Delete" color="danger" @click="deleteCollection" :loading="databaseStore.loading" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Collections table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="p-4 border-b">
          <div class="flex justify-between items-center">
            <h3 class="font-semibold">
              Collections
              <span v-if="selectedDatabase" class="text-gray-500 text-sm font-normal ml-2">
                in {{ selectedDatabase }}
              </span>
            </h3>
            <div class="text-sm text-gray-500">
              {{ databaseStore.collectionCount }} collections
            </div>
          </div>
        </div>
        
        <div v-if="!selectedDatabase" class="p-12 flex flex-col items-center justify-center text-gray-500">
          <q-icon name="folder_open" size="64px" class="mb-4" />
          <p>Please select a database to view collections</p>
        </div>
        
        <div v-else-if="databaseStore.collectionsLoading" class="p-12 flex justify-center items-center">
          <q-spinner size="48px" color="primary" />
        </div>
        
        <div v-else-if="databaseStore.collections.length === 0" class="p-12 flex flex-col items-center justify-center text-gray-500">
          <q-icon name="inbox" size="64px" class="mb-4" />
          <p>No collections found in {{ selectedDatabase }}</p>
          <q-btn 
            label="Create First Collection" 
            color="primary" 
            @click="showCreateForm = true"
            :disabled="!authStore.isAuthenticated"
            class="mt-4"
          />
        </div>
        
        <div v-if="databaseStore.collections.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-100">
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Collection Name</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(collection, index) in databaseStore.collections" :key="index">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center gap-3">
                    <q-icon name="folder" color="secondary" />
                    <span class="font-medium">{{ collection }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <div class="flex items-center justify-end gap-2">
                    <router-link 
                      :to="{ path: '/documents', query: { db: selectedDatabase, coll: collection } }"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                    >
                      <span>View Documents</span>
                    </router-link>
                    <button 
                      @click="confirmDelete(collection)"
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
const showCreateForm = ref(false);
const newCollectionName = ref('');
const showDeleteDialog = ref(false);
const collectionToDelete = ref('');

// Fetch databases on mount
onMounted(async () => {
  await databaseStore.fetchDatabases();
  
  // Check if database is passed from route params
  const dbParam = route.query.db as string;
  if (dbParam && databaseStore.databases.includes(dbParam)) {
    selectedDatabase.value = dbParam;
    await databaseStore.fetchCollections(dbParam);
  }
});

// Watch for route changes
watch(() => route.query.db, async (newDb) => {
  if (newDb && databaseStore.databases.includes(newDb as string)) {
    selectedDatabase.value = newDb as string;
    await databaseStore.fetchCollections(newDb as string);
  }
});

// Handle database change
async function onDatabaseChange(database: string | null) {
  if (database) {
    await databaseStore.fetchCollections(database);
  } else {
    databaseStore.setCurrentDatabase(null);
  }
}

// Fetch collections
async function fetchCollections() {
  if (selectedDatabase.value) {
    await databaseStore.fetchCollections(selectedDatabase.value);
  }
}

// Show delete confirmation
function confirmDelete(collection: string) {
  collectionToDelete.value = collection;
  showDeleteDialog.value = true;
}

// Create collection
async function createCollection() {
  if (!newCollectionName.value || !selectedDatabase.value) return;
  
  try {
    const collName = newCollectionName.value;
    const dbName = selectedDatabase.value;
    await databaseStore.createCollection(dbName, collName);
    showCreateForm.value = false;
    newCollectionName.value = '';
    notificationService.success(`Collection ${collName} created successfully in ${dbName}`);
  } catch (error) {
    console.error('Error creating collection:', error);
    notificationService.error(`Failed to create collection: ${String(error)}`);
  }
}

// Delete collection
async function deleteCollection() {
  if (!collectionToDelete.value || !selectedDatabase.value) return;
  
  try {
    const collName = collectionToDelete.value;
    const dbName = selectedDatabase.value;
    await databaseStore.deleteCollection(dbName, collName);
    showDeleteDialog.value = false;
    collectionToDelete.value = '';
    notificationService.success(`Collection ${collName} deleted successfully from ${dbName}`);
  } catch (error) {
    console.error('Error deleting collection:', error);
    notificationService.error(`Failed to delete collection: ${String(error)}`);
  }
}
</script>

<style scoped>
/* Add custom styles here */
.btn-visible-text {
  color: #ffffff !important;
  font-weight: 500 !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

.btn-visible-text:disabled {
  color: rgba(255, 255, 255, 0.8) !important;
}
</style>