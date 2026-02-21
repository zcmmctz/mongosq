<template>
  <q-page class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <!-- Page header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Database Management</h1>
          <p class="text-gray-600">Manage your MongoDB databases</p>
        </div>
        
        <q-btn 
          label="Create Database" 
          color="primary" 
          icon="add" 
          @click="showCreateForm = true"
          :disabled="!authStore.isAuthenticated"
        />
      </div>

      <!-- Authentication warning -->
      <div v-if="!authStore.isAuthenticated" class="bg-warning/20 border border-warning rounded-lg p-4 mb-6">
        <div class="flex items-center gap-3">
          <q-icon name="warning" color="warning" />
          <div>
            <h3 class="font-medium text-warning">Authentication Required</h3>
            <p class="text-sm text-gray-700">
              You need to set an API key in settings to create or delete databases
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
      <div v-if="databaseStore.databasesError" class="bg-danger/20 border border-danger rounded-lg p-4 mb-6">
        <div class="flex items-center gap-3">
          <q-icon name="error" color="danger" />
          <div>
            <h3 class="font-medium text-danger">Error</h3>
            <p class="text-sm text-gray-700">{{ databaseStore.databasesError }}</p>
            <q-btn 
              label="Retry" 
              size="sm" 
              color="danger" 
              @click="fetchDatabases" 
              class="mt-2"
            />
          </div>
        </div>
      </div>

      <!-- Create database form -->
      <q-dialog v-model="showCreateForm" persistent>
        <q-card class="w-full max-w-md">
          <q-card-section>
            <h2 class="text-xl font-bold">Create New Database</h2>
          </q-card-section>
          
          <q-card-section>
            <q-form @submit="createDatabase">
              <q-input
                v-model="newDatabaseName"
                label="Database Name"
                placeholder="Enter database name"
                :rules="[val => !!val || 'Database name is required']"
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
            <h2 class="text-xl font-bold">Delete Database</h2>
          </q-card-section>
          
          <q-card-section>
            <p>Are you sure you want to delete the database <strong>{{ databaseToDelete }}</strong>? This action cannot be undone.</p>
          </q-card-section>
          
          <q-card-actions align="right" class="gap-2">
            <q-btn label="Cancel" @click="showDeleteDialog = false" />
            <q-btn label="Delete" color="danger" @click="deleteDatabase" :loading="databaseStore.loading" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Databases table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="p-4 border-b">
          <div class="flex justify-between items-center">
            <h3 class="font-semibold">Databases</h3>
            <div class="text-sm text-gray-500">
              {{ databaseStore.databaseCount }} databases
            </div>
          </div>
        </div>
        
        <div v-if="databaseStore.databasesLoading" class="p-12 flex justify-center items-center">
          <q-spinner size="48px" color="primary" />
        </div>
        
        <div v-else-if="databaseStore.databases.length === 0" class="p-12 flex flex-col items-center justify-center text-gray-500">
          <q-icon name="inbox" size="64px" class="mb-4" />
          <p>No databases found</p>
          <q-btn 
            label="Create First Database" 
            color="primary" 
            @click="showCreateForm = true"
            :disabled="!authStore.isAuthenticated"
            class="mt-4"
          />
        </div>
        
        <div v-if="databaseStore.databases.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-100">
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Database Name</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(database, index) in databaseStore.databases" :key="index">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center gap-3">
                    <q-icon name="database" color="primary" />
                    <span class="font-medium">{{ database }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <div class="flex items-center justify-end gap-2">
                    <router-link 
                      :to="{ path: '/collections', query: { db: database } }"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      <span>View Collections</span>
                    </router-link>
                    <button 
                      @click="confirmDelete(database)"
                      :disabled="!authStore.isAuthenticated"
                      class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
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
import { ref, onMounted } from 'vue';
import { useDatabaseStore } from '../stores/database';
import { useAuthStore } from '../stores/auth';
import { notificationService } from '../services/notification';

const databaseStore = useDatabaseStore();
const authStore = useAuthStore();

// Form state
const showCreateForm = ref(false);
const newDatabaseName = ref('');

// Delete state
const showDeleteDialog = ref(false);
const databaseToDelete = ref('');

// Fetch databases on mount
onMounted(async () => {
  await fetchDatabases();
});

// Fetch databases
async function fetchDatabases() {
  try {
    await databaseStore.fetchDatabases();
  } catch (error) {
    console.error('Error fetching databases:', error);
  }
}

// Show delete confirmation
function confirmDelete(database: string) {
  databaseToDelete.value = database;
  showDeleteDialog.value = true;
}

// Create database
async function createDatabase() {
  if (!newDatabaseName.value) return;
  
  try {
    const dbName = newDatabaseName.value;
    await databaseStore.createDatabase(dbName);
    showCreateForm.value = false;
    newDatabaseName.value = '';
    notificationService.success(`Database ${dbName} created successfully`);
  } catch (error) {
    console.error('Error creating database:', error);
    notificationService.error(`Failed to create database: ${String(error)}`);
  }
}

// Delete database
async function deleteDatabase() {
  if (!databaseToDelete.value) return;
  
  try {
    await databaseStore.deleteDatabase(databaseToDelete.value);
    showDeleteDialog.value = false;
    notificationService.success(`Database ${databaseToDelete.value} deleted successfully`);
    databaseToDelete.value = '';
  } catch (error) {
    console.error('Error deleting database:', error);
    notificationService.error(`Failed to delete database: ${String(error)}`);
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