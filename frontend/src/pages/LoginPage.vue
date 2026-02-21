<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6 text-gray-800">MongoDB Manager Login</h1>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="account" class="block text-sm font-medium text-gray-700 mb-1">Account</label>
          <input
            type="text"
            id="account"
            v-model="loginForm.account"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your account"
            required
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            type="password"
            id="password"
            v-model="loginForm.password"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password"
            required
          />
        </div>
        
        <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded-md">
          {{ error }}
        </div>
        
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          :disabled="loading"
        >
          <span v-if="loading">Logging in...</span>
          <span v-else>Login</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../services/api';

const router = useRouter();
const loginForm = ref({
  account: '',
  password: ''
});
const error = ref('');
const loading = ref(false);

const handleLogin = async () => {
  error.value = '';
  loading.value = true;
  
  try {
    // Call login API using apiService
    const data = await apiService.login(loginForm.value.account, loginForm.value.password);
    
    // Save API key to localStorage
    apiService.setApiKey(data.access_token);
    
    // Redirect to home page
    await router.push('/');
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An unknown error occurred';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Add any component-specific styles here */
</style>