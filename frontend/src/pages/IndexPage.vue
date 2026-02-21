<template>
  <q-page class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <!-- Hero section -->
      <div class="bg-primary text-white rounded-lg shadow-lg p-8 mb-8">
        <h1 class="text-3xl font-bold mb-4">Welcome to MongoDB Manager</h1>
        <p class="text-lg opacity-90">
          A powerful tool for managing your MongoDB databases and collections
        </p>
      </div>

      <!-- Features section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-primary">
          <div class="text-primary text-4xl mb-4">
            <q-icon name="database" size="48px" />
          </div>
          <h3 class="text-xl font-semibold mb-2">Database Management</h3>
          <p class="text-gray-600">
            Create, delete, and manage your MongoDB databases with ease
          </p>
          <router-link 
            to="/databases"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 mt-4"
          >
            Manage Databases
          </router-link>
        </div>

        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-secondary">
          <div class="text-secondary text-4xl mb-4">
            <q-icon name="folder" size="48px" />
          </div>
          <h3 class="text-xl font-semibold mb-2">Collection Management</h3>
          <p class="text-gray-600">
            Organize and manage collections within your databases
          </p>
          <router-link 
            to="/collections"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 mt-4"
          >
            Manage Collections
          </router-link>
        </div>

        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-success">
          <div class="text-success text-4xl mb-4">
            <q-icon name="settings" size="48px" />
          </div>
          <h3 class="text-xl font-semibold mb-2">Settings</h3>
          <p class="text-gray-600">
            Configure API settings and authentication
          </p>
          <router-link 
            to="/settings"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 mt-4"
          >
            Configure Settings
          </router-link>
        </div>
      </div>

      <!-- Status section -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">System Status</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-center gap-4 p-4 border rounded-lg">
            <div class="text-success">
              <q-icon name="check_circle" size="24px" />
            </div>
            <div>
              <h4 class="font-medium">Frontend</h4>
              <p class="text-gray-600">Ready</p>
            </div>
          </div>
          <div class="flex items-center gap-4 p-4 border rounded-lg">
            <div class="text-warning">
              <q-icon name="info" size="24px" />
            </div>
            <div>
              <h4 class="font-medium">Backend</h4>
              <p class="text-gray-600">Checking connection...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Home page component
</script>

<style scoped>
/* Add custom styles here */
</style>
