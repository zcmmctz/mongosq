<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" class="text-white" />

        <q-toolbar-title class="text-white"> MongoDB Manager </q-toolbar-title>

        <div class="flex items-center gap-4">
          <q-avatar size="32px" class="bg-white text-primary font-bold">
            <span>M</span>
          </q-avatar>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-gray-50">
      <q-list>
        <q-item-label header class="bg-primary text-white"> MongoDB Management </q-item-label>

        <q-item to="/" clickable active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>
            <q-item-label> Home </q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/databases" clickable active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="database" />
          </q-item-section>
          <q-item-section>
            <q-item-label> Databases </q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/collections" clickable active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="folder" />
          </q-item-section>
          <q-item-section>
            <q-item-label> Collections </q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/settings" clickable active-class="bg-primary text-white">
          <q-item-section avatar>
            <q-icon name="settings" />
          </q-item-section>
          <q-item-section>
            <q-item-label> Settings </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="my-2" />

        <q-item-label header> About </q-item-label>

        <q-item clickable>
          <q-item-section avatar>
            <q-icon name="info" />
          </q-item-section>
          <q-item-section>
            <q-item-label> About MongoDB Manager </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const leftDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

<style scoped>
/* Add custom styles here */
</style>
