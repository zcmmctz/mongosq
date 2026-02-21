import { defineStore } from 'pinia';
import { apiService } from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    apiKey: apiService.getApiKey(),
    isAuthenticated: !!apiService.getApiKey(),
    loading: false,
    error: null as string | null
  }),

  getters: {
    hasApiKey: (state) => !!state.apiKey,
    authStatus: (state) => state.isAuthenticated
  },

  actions: {
    /**
     * Set API key and update authentication status
     */
    setApiKey(key: string) {
      try {
        this.loading = true;
        this.error = null;
        
        apiService.setApiKey(key);
        this.apiKey = key;
        this.isAuthenticated = true;
        
        return true;
      } catch (error) {
        this.error = `Failed to set API key: ${String(error)}`;
        return false;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Remove API key and update authentication status
     */
    removeApiKey() {
      try {
        this.loading = true;
        
        apiService.removeApiKey();
        this.apiKey = null;
        this.isAuthenticated = false;
        this.error = null;
        
        return true;
      } catch (error) {
        this.error = `Failed to remove API key: ${String(error)}`;
        return false;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Clear error message
     */
    clearError() {
      this.error = null;
    }
  }
});
