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

      <!-- DaisyUI Tabs -->
      <div class="tabs tabs-lifted">
        <!-- Users Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="👥 Users" :checked="true" />
        <UserTable
          :users="users || []"
          @delete="handleDeleteUser"
        />

        <!-- Organizations Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="🏢 Organizations" />
        <OrganizationTable
          :organizations="organizations || []"
          @delete="handleDeleteOrganization"
        />

        <!-- Campaigns Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📢 Campaigns" />
        <CampaignTable
          :campaigns="campaigns || []"
          :organizations="organizations || []"
          :selected-organization-id="selectedOrganizationId"
          @delete="handleDeleteCampaign"
          @update-organization-filter="handleUpdateOrganizationFilter"
        />

        <!-- Applications Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📋 Applications" v-on:click="onApplicationSelected"/>
        <ApplicationsTable
          :campaigns="campaigns || []"
          :users="users || []"
          @delete="handleDeleteApplication"
        />

        <!-- Publications Tab -->
        <input type="radio" name="db_tabs" class="tab" aria-label="📰 Publications" />
        <PublicationTable
          :accounts="accounts || []"
          @delete="handleDeletePublication"
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
import PublicationTable from './PublicationTable.vue'
import { useUsersQuery, useOrganizationsQuery, useCampaignsQuery, useAccountsQuery } from '@/hooks/queries'
import type { User, Organization, CampaignData, Application, Publication } from '../types'

// Organization filter for campaigns (null = all campaigns)
const selectedOrganizationId = ref<number | null>(null)

// Fetch data using query hooks
const { data: users } = useUsersQuery()
const { data: organizations } = useOrganizationsQuery()
const { data: campaigns } = useCampaignsQuery(selectedOrganizationId)
const { data: accounts } = useAccountsQuery()

// Event handlers for delete operations (create/edit handled internally)
const handleDeleteUser = (user: User) => {
  console.log('Delete user', user)
}

const handleDeleteOrganization = (organization: Organization) => {
  console.log('Delete organization', organization)
}

const handleDeleteCampaign = (campaign: CampaignData) => {
  console.log('Delete campaign', campaign)
}

const handleDeleteApplication = (application: Application) => {
  console.log('Delete application', application)
}

const handleDeletePublication = (publication: Publication) => {
  console.log('Delete publication', publication)
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
