<template>
  <div class="min-h-screen bg-base-200 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold mb-2 text-primary">
          Database Management
        </h1>
        <p class="text-base-content text-lg">Manage your data with ease</p>
      </div>

      <!-- Database Selection -->
      <div class="mb-6">
        <div class="flex items-center gap-4">
          <label class="text-base-content font-medium">Database:</label>
          <select v-model="selectedDatabase" class="select select-bordered select-primary w-64">
            <option value="postgres">🐘 PostgreSQL</option>
            <option value="duckdb">🦆 DuckDB</option>
            <option value="scylla">⚡ ScyllaDB</option>
          </select>
          <div class="badge badge-outline badge-primary">
            {{ selectedDatabase.toUpperCase() }}
          </div>
        </div>
      </div>

      <!-- DaisyUI Tabs -->
      <div class="tabs tabs-lifted">
        <!-- Users Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="👥 Users" :checked="true" />
        <UserTable
          :users="users || []"
          :selected-database="selectedDatabase"
          @delete="handleDeleteUser"
        />

        <!-- Organizations Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="🏢 Organizations" />
        <OrganizationTable
          :organizations="organizations || []"
          :selected-database="selectedDatabase"
          @delete="handleDeleteOrganization"
        />

        <!-- Campaigns Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📢 Campaigns" />
        <CampaignTable
          :campaigns="campaigns || []"
          :organizations="organizations || []"
          :selected-database="selectedDatabase"
          :selected-organization-id="selectedOrganizationId"
          @delete="handleDeleteCampaign"
          @update-organization-filter="handleUpdateOrganizationFilter"
        />

        <!-- Applications Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📋 Applications" v-on:click="onApplicationSelected"/>
        <ApplicationsTable
          :campaigns="campaigns || []"
          :users="users || []"
          :selected-database="selectedDatabase"
          @delete="handleDeleteApplication"
        />
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useQueryClient } from '@tanstack/vue-query'
import UserTable from './UserTable.vue'
import OrganizationTable from './OrganizationTable.vue'
import CampaignTable from './CampaignTable.vue'
import ApplicationsTable from './ApplicationsTable.vue'
import { useUsersQuery, useOrganizationsQuery, useCampaignsQuery } from '@/hooks/queries'
import type { User, Organization, CampaignData, Application, DatabaseType } from '../types'

const selectedDatabase = ref<DatabaseType>('postgres')

// Get query client for invalidating queries
const queryClient = useQueryClient()

// Organization filter for campaigns (null = all campaigns)
const selectedOrganizationId = ref<number | null>(null)

// Watch for database changes and invalidate all queries
watch(selectedDatabase, async (newDb, oldDb) => {
  if (newDb !== oldDb) {
    await queryClient.invalidateQueries()
  }
})

// Fetch data using query hooks
const { data: users } = useUsersQuery(selectedDatabase)
const { data: organizations } = useOrganizationsQuery(selectedDatabase)
const { data: campaigns } = useCampaignsQuery(selectedDatabase, selectedOrganizationId)

// Event handlers for delete operations (create/edit handled internally)
const handleDeleteUser = (user: User) => {
  console.log('Delete user', user, selectedDatabase.value)
}

const handleDeleteOrganization = (organization: Organization) => {
  console.log('Delete organization', organization, selectedDatabase.value)
}

const handleDeleteCampaign = (campaign: CampaignData) => {
  console.log('Delete campaign', campaign, selectedDatabase.value)
}

const handleDeleteApplication = (application: Application) => {
  console.log('Delete application', application, selectedDatabase.value)
}

// Organization filter handler for campaigns
const handleUpdateOrganizationFilter = (organizationId: number | null) => {
  selectedOrganizationId.value = organizationId
}

function onApplicationSelected(){
  selectedOrganizationId.value = null;
}
</script>

<style scoped>
/* Clean, minimal styling */
</style>
