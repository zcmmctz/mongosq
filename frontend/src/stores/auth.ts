import { defineStore } from 'pinia';
import { apiService } from '../services/api';

interface AuthState {
  apiKey: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    apiKey: apiService.getApiKey(),
    isAuthenticated: !!apiService.getApiKey(),
    loading: false,
    error: null
  }),

  getters: {
    hasApiKey: (state: AuthState) => !!state.apiKey,
    authStatus: (state: AuthState) => state.isAuthenticated
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
