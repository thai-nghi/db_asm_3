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
        <input type="radio" name="db_tabs" class="tab" aria-label="👥 Users (5)" checked="checked" />
        <UserTable
          :users="users"
          :selected-database="selectedDatabase"
          @add="handleAddUser"
          @edit="handleEditUser"
          @delete="handleDeleteUser"
        />

        <!-- Organizations Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="🏢 Organizations (4)" />
        <OrganizationTable
          :organizations="organizations"
          :selected-database="selectedDatabase"
          @add="handleAddOrganization"
          @edit="handleEditOrganization"
          @delete="handleDeleteOrganization"
        />

        <!-- Campaigns Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📢 Campaigns (6)" />
        <CampaignTable
          :campaigns="campaigns"
          :selected-database="selectedDatabase"
          @add="handleAddCampaign"
          @edit="handleEditCampaign"
          @delete="handleDeleteCampaign"
        />

        <!-- Applications Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📋 Applications (8)" />
        <ApplicationsTable
          :applications="applications"
          :selected-database="selectedDatabase"
          @add="handleAddApplication"
          @edit="handleEditApplication"
          @delete="handleDeleteApplication"
        />
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import UserTable from './UserTable.vue'
import OrganizationTable from './OrganizationTable.vue'
import CampaignTable from './CampaignTable.vue'
import ApplicationsTable from './ApplicationsTable.vue'

// Interfaces based on schemas.py
interface User {
  id: number
  username: string
  email: string
}

interface Organization {
  id: number
  name: string
}

interface CampaignData {
  id: number
  organizer_id: number
  name: string
}

interface Application {
  id: number
  campaign_id: number
  user_id: number
  status: 'PENDING' | 'APPROVED' | 'REJECTED'
}

// Database selection
type DatabaseType = 'postgres' | 'duckdb' | 'scylla'
const selectedDatabase = ref<DatabaseType>('postgres')

// Mock data
const users = ref<User[]>([
  { id: 1, username: 'john_doe', email: 'john@example.com' },
  { id: 2, username: 'jane_smith', email: 'jane@example.com' },
  { id: 3, username: 'mike_wilson', email: 'mike@example.com' },
  { id: 4, username: 'sarah_connor', email: 'sarah@example.com' },
  { id: 5, username: 'alex_jones', email: 'alex@example.com' }
])

const organizations = ref<Organization[]>([
  { id: 1, name: 'Tech Corp' },
  { id: 2, name: 'Marketing Agency' },
  { id: 3, name: 'Startup Inc' },
  { id: 4, name: 'Global Solutions' }
])

const campaigns = ref<CampaignData[]>([
  { id: 1, organizer_id: 1, name: 'Summer Product Launch' },
  { id: 2, organizer_id: 2, name: 'Brand Awareness Campaign' },
  { id: 3, organizer_id: 1, name: 'Holiday Sales Push' },
  { id: 4, organizer_id: 3, name: 'New User Acquisition' },
  { id: 5, organizer_id: 4, name: 'Customer Retention Drive' },
  { id: 6, organizer_id: 2, name: 'Social Media Boost' }
])

const applications = ref<Application[]>([
  { id: 1, campaign_id: 1, user_id: 1, status: 'PENDING' },
  { id: 2, campaign_id: 1, user_id: 2, status: 'APPROVED' },
  { id: 3, campaign_id: 2, user_id: 3, status: 'REJECTED' },
  { id: 4, campaign_id: 2, user_id: 4, status: 'PENDING' },
  { id: 5, campaign_id: 3, user_id: 5, status: 'APPROVED' },
  { id: 6, campaign_id: 3, user_id: 1, status: 'PENDING' },
  { id: 7, campaign_id: 4, user_id: 2, status: 'APPROVED' },
  { id: 8, campaign_id: 5, user_id: 3, status: 'REJECTED' }
])

// Event handlers for User operations
const handleAddUser = () => {
  console.log('Add user', selectedDatabase.value)
}

const handleEditUser = (user: User) => {
  console.log('Edit user', user, selectedDatabase.value)
}

const handleDeleteUser = (user: User) => {
  console.log('Delete user', user, selectedDatabase.value)
}

// Event handlers for Organization operations
const handleAddOrganization = () => {
  console.log('Add organization', selectedDatabase.value)
}

const handleEditOrganization = (organization: Organization) => {
  console.log('Edit organization', organization, selectedDatabase.value)
}

const handleDeleteOrganization = (organization: Organization) => {
  console.log('Delete organization', organization, selectedDatabase.value)
}

// Event handlers for Campaign operations
const handleAddCampaign = () => {
  console.log('Add campaign', selectedDatabase.value)
}

const handleEditCampaign = (campaign: CampaignData) => {
  console.log('Edit campaign', campaign, selectedDatabase.value)
}

const handleDeleteCampaign = (campaign: CampaignData) => {
  console.log('Delete campaign', campaign, selectedDatabase.value)
}

// Event handlers for Application operations
const handleAddApplication = () => {
  console.log('Add application', selectedDatabase.value)
}

const handleEditApplication = (application: Application) => {
  console.log('Edit application', application, selectedDatabase.value)
}

const handleDeleteApplication = (application: Application) => {
  console.log('Delete application', application, selectedDatabase.value)
}
</script>

<style scoped>
/* Clean, minimal styling */
</style>
