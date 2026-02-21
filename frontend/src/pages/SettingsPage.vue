<template>
  <q-page class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <!-- Page header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Settings</h1>
        <p class="text-gray-600">Configure MongoDB Manager settings</p>
      </div>

      <!-- API Key settings -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">API Key Configuration</h2>
        
        <div v-if="authStore.error" class="bg-danger/20 border border-danger rounded-lg p-4 mb-4">
          <div class="flex items-center gap-3">
            <q-icon name="error" color="danger" />
            <div>
              <h3 class="font-medium text-danger">Error</h3>
              <p class="text-sm text-gray-700">{{ authStore.error }}</p>
            </div>
          </div>
        </div>

        <q-form @submit="saveApiKey">
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">API Key</label>
            <q-input
              v-model="apiKeyInput"
              type="password"
              label="API Key"
              placeholder="Enter your API key"
              :rules="[val => !!val || 'API key is required']"
            />
            <p class="text-sm text-gray-500 mt-2">
              The API key is required for creating and deleting databases and collections.
            </p>
          </div>

          <div class="flex justify-end gap-2">
            <q-btn label="Cancel" @click="cancelEdit" />
            <q-btn label="Save" color="primary" type="submit" :loading="authStore.loading" />
          </div>
        </q-form>

        <div v-if="authStore.isAuthenticated" class="mt-4 p-4 bg-success/10 border border-success rounded-lg">
          <div class="flex items-center gap-3">
            <q-icon name="check_circle" color="success" />
            <div>
              <h3 class="font-medium text-success">API Key Set</h3>
              <p class="text-sm text-gray-700">You are authenticated and can perform write operations.</p>
              <q-btn 
                label="Remove API Key" 
                size="sm" 
                color="danger" 
                @click="removeApiKey" 
                class="mt-2"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Database Connection settings -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Database Connection Configuration</h2>
        
        <div v-if="databaseStore.connectionSettingsError" class="bg-danger/20 border border-danger rounded-lg p-4 mb-4">
          <div class="flex items-center gap-3">
            <q-icon name="error" color="danger" />
            <div>
              <h3 class="font-medium text-danger">Error</h3>
              <p class="text-sm text-gray-700">{{ databaseStore.connectionSettingsError }}</p>
            </div>
          </div>
        </div>

        <q-form @submit="saveConnectionSettings">
          <div class="space-y-4">
            <div>
              <label class="block text-gray-700 font-medium mb-2">MongoDB Connection URI</label>
              <q-input
                v-model="connectionSettings.mongodb_uri"
                label="MongoDB Connection URI"
                placeholder="mongodb://localhost:27017"
                :rules="[val => !!val || 'Connection URI is required']"
              />
              <p class="text-sm text-gray-500 mt-2">
                The connection string for your MongoDB server. Example: mongodb://username:password@host:port
              </p>
            </div>

            <div>
              <label class="block text-gray-700 font-medium mb-2">Database Name</label>
              <q-input
                v-model="connectionSettings.mongodb_db_name"
                label="Database Name"
                placeholder="admin"
                :rules="[val => !!val || 'Database name is required']"
              />
              <p class="text-sm text-gray-500 mt-2">
                The default database to connect to.
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-gray-700 font-medium mb-2">Max Pool Size</label>
                <q-input
                  v-model.number="connectionSettings.mongodb_max_pool_size"
                  type="number"
                  label="Max Pool Size"
                  placeholder="100"
                  :rules="[val => !!val || 'Max pool size is required', val => !isNaN(val) || 'Must be a number']"
                />
              </div>

              <div>
                <label class="block text-gray-700 font-medium mb-2">Min Pool Size</label>
                <q-input
                  v-model.number="connectionSettings.mongodb_min_pool_size"
                  type="number"
                  label="Min Pool Size"
                  placeholder="10"
                  :rules="[val => !!val || 'Min pool size is required', val => !isNaN(val) || 'Must be a number']"
                />
              </div>

              <div>
                <label class="block text-gray-700 font-medium mb-2">Max Idle Time (ms)</label>
                <q-input
                  v-model.number="connectionSettings.mongodb_max_idle_time_ms"
                  type="number"
                  label="Max Idle Time"
                  placeholder="300000"
                  :rules="[val => !!val || 'Max idle time is required', val => !isNaN(val) || 'Must be a number']"
                />
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-2 mt-4">
            <q-btn label="Cancel" @click="cancelConnectionSettingsEdit" />
            <q-btn label="Save" color="primary" type="submit" :loading="databaseStore.connectionSettingsLoading" />
          </div>
        </q-form>

        <div v-if="databaseStore.connected" class="mt-4 p-4 bg-success/10 border border-success rounded-lg">
          <div class="flex items-center gap-3">
            <q-icon name="check_circle" color="success" />
            <div>
              <h3 class="font-medium text-success">Connected</h3>
              <p class="text-sm text-gray-700">Successfully connected to MongoDB server.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- About section -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">About</h2>
        <div class="space-y-4">
          <div>
            <h3 class="font-medium">MongoDB Manager</h3>
            <p class="text-gray-600">Version 1.0.0</p>
          </div>
          <div>
            <h3 class="font-medium">Description</h3>
            <p class="text-gray-600">
              A web-based tool for managing MongoDB databases and collections, built with Vue 3, Quasar, and Tailwind CSS.
            </p>
          </div>
          <div>
            <h3 class="font-medium">Backend API</h3>
            <p class="text-gray-600">
              API Base URL: <span class="font-mono">http://localhost:22222</span>
            </p>
            <p class="text-gray-600 mt-2">
              API Documentation: <a href="http://localhost:22222/docs" target="_blank" class="text-primary underline">http://localhost:22222/docs</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useDatabaseStore } from '../stores/database';
import { notificationService } from '../services/notification';

const authStore = useAuthStore();
const databaseStore = useDatabaseStore();
const apiKeyInput = ref('');
const connectionSettings = reactive({
  mongodb_uri: 'mongodb://localhost:27017',
  mongodb_db_name: 'admin',
  mongodb_max_pool_size: 100,
  mongodb_min_pool_size: 10,
  mongodb_max_idle_time_ms: 300000
});

// Initialize form with current API key and connection settings
onMounted(async () => {
  // Don't prefill the API key for security reasons
  apiKeyInput.value = '';
  
  // Load current connection settings
  await loadConnectionSettings();
});

// Load connection settings
async function loadConnectionSettings() {
  try {
    const settings = await databaseStore.fetchConnectionSettings();
    Object.assign(connectionSettings, settings);
  } catch (error) {
    console.error('Error loading connection settings:', error);
  }
}

// Save API key
function saveApiKey() {
  try {
    const success = authStore.setApiKey(apiKeyInput.value);
    if (success) {
      // Clear input after saving
      apiKeyInput.value = '';
      notificationService.success('API key saved successfully');
    }
  } catch (error) {
    console.error('Error saving API key:', error);
    notificationService.error(`Failed to save API key: ${String(error)}`);
  }
}

// Remove API key
function removeApiKey() {
  authStore.removeApiKey();
  apiKeyInput.value = '';
  notificationService.success('API key removed successfully');
}

// Cancel edit
function cancelEdit() {
  apiKeyInput.value = '';
  authStore.clearError();
}

// Save connection settings
async function saveConnectionSettings() {
  try {
    await databaseStore.updateConnectionSettings(connectionSettings);
    notificationService.success('Database connection settings saved successfully');
  } catch (error) {
    console.error('Error saving connection settings:', error);
    notificationService.error(`Failed to save connection settings: ${String(error)}`);
  }
}

// Cancel connection settings edit
async function cancelConnectionSettingsEdit() {
  await loadConnectionSettings();
  databaseStore.connectionSettingsError = null;
}
</script>

<style scoped>
/* Add custom styles here */
</style>