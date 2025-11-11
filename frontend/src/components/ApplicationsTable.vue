<template>
  <div class="tab-content">
    <!-- Filter Section -->
    <div class="mb-4">
      <div class="flex items-center gap-4 flex-wrap">
        <!-- Campaign Filter -->
        <div class="flex items-center gap-2">
          <label class="text-base-content font-medium">Campaign:</label>
          <select v-model="selectedCampaignId" class="select select-bordered select-neutral w-48">
            <option :value="null">All Campaigns</option>
            <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">
              {{ campaign.name }}
            </option>
          </select>
        </div>
        
        <!-- User Filter -->
        <div class="flex items-center gap-2">
          <label class="text-base-content font-medium">User:</label>
          <select v-model="selectedUserId" class="select select-bordered select-neutral w-48">
            <option :value="null">All Users</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>
        
        <!-- Active Filter Badges -->
        <div class="flex gap-2">
          <div v-if="selectedCampaignId !== null" class="badge badge-outline badge-neutral">
            Campaign: {{ getCampaignName(selectedCampaignId) }}
          </div>
          <div v-if="selectedUserId !== null" class="badge badge-outline badge-neutral">
            User: {{ getUserName(selectedUserId) }}
          </div>
        </div>
      
      </div>
    </div>

    <!-- Table -->
    <BaseTable
      title="Applications"
      :data="applicationData"
      :columns="columns"
      :icon="FileDocumentIcon"
      add-button-text="Add Application"
      border-class="border-neutral"
      icon-bg-class="bg-neutral/10"
      icon-color-class="text-neutral"
      button-class="btn-neutral"
      @add="openCreateModal"
      @edit="openEditModal"
      @delete="handleDelete"
    >
      <template #cell-campaign_id="{ value }">
        <span class="text-neutral font-medium">{{ getCampaignName(value) }}</span>
      </template>
      <template #cell-user_id="{ value }">
        <span class="text-neutral font-medium">{{ getUserName(value) }}</span>
      </template>
      <template #cell-status="{ value }">
        <div class="badge"
          :class="{
            'badge-success': value === 'APPROVED',
            'badge-error': value === 'REJECTED',
            'badge-warning': value === 'PENDING'
          }"
        >
          {{ value }}
        </div>
      </template>
    </BaseTable>
  </div>

  <!-- Create/Edit Modal -->
  <dialog ref="applicationModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ isEditing ? 'Edit Application' : 'Create New Application' }}
      </h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-4 mt-4">
        <!-- Campaign field -->
        <div>
          <label class="label">
            <span class="label-text">Campaign</span>
          </label>
          <select
            v-model="formData.campaign_id"
            class="select select-bordered w-full"
            required
          >
            <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">
              {{ campaign.name }}
            </option>
          </select>
        </div>

        <!-- User field -->
        <div>
          <label class="label">
            <span class="label-text">User</span>
          </label>
          <select
            v-model="formData.user_id"
            class="select select-bordered w-full"
            required
          >
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }} ({{ user.email }})
            </option>
          </select>
        </div>

        <!-- Status field -->
        <div v-if="isEditing">
          <label class="label">
            <span class="label-text">Status</span>
          </label>
          <select
            v-model="formData.status"
            class="select select-bordered w-full"
            required
          >
            <option value="pending">Pending</option>
            <option value="accept">Accepted</option>
            <option value="declined">Declined</option>
          </select>
        </div>

        <!-- Modal Actions -->
        <div class="modal-action">
          <button
            type="button"
            class="btn btn-ghost"
            @click="closeModal"
            :disabled="isSubmitting"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn btn-neutral"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="loading loading-spinner loading-sm"></span>
            {{ isEditing ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button type="button" @click="closeModal">close</button>
    </form>
  </dialog>
</template>

<script setup lang="ts">
import { ref, computed, reactive, watch, type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import FileDocumentIcon from 'vue-material-design-icons/FileDocument.vue'
import { useApplicationsQuery } from '@/hooks/queries'
import { useCreateApplicationMutation, useUpdateApplicationMutation } from '@/hooks/mutations'
import type { Application, CampaignData, User, DatabaseType } from '../types'
import type { ApplicationStatus } from '@/api'

const props = defineProps({
  campaigns: {
    type: Array as PropType<CampaignData[]>,
    required: true,
  },
  users: {
    type: Array as PropType<User[]>,
    required: true,
  },
  selectedDatabase: {
    type: String as PropType<DatabaseType>,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'delete', application: Application): void
}>()

// Database type reactive ref
const dbTypeRef = ref(props.selectedDatabase)

// Watch for database changes
watch(() => props.selectedDatabase, (newDb) => {
  dbTypeRef.value = newDb
})

// Filter state
const selectedCampaignId = ref<number | null>(null)
const selectedUserId = ref<number | null>(null)

// Query for applications with backend filtering
const { data: applications } = useApplicationsQuery(
  dbTypeRef,
  selectedCampaignId,
  selectedUserId
)

// Computed property to ensure we always have an array
const applicationData = computed(() => applications.value || [])

// Modal refs and state
const applicationModal = ref<HTMLDialogElement>()
const isEditing = ref(false)
const editingApplication = ref<Application | null>(null)

// Form data
const formData = reactive({
  campaign_id: null as number | null,
  user_id: null as number | null,
  status: 'pending' as ApplicationStatus | '',
})

// Mutations
const createApplicationMutation = useCreateApplicationMutation(dbTypeRef)
const updateApplicationMutation = useUpdateApplicationMutation(dbTypeRef)

// Computed properties
const isSubmitting = computed(() => 
  createApplicationMutation.isPending.value || updateApplicationMutation.isPending.value
)

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-neutral' },
  { key: 'campaign_id', label: 'Campaign', type: 'text' as const },
  { key: 'user_id', label: 'User', type: 'text' as const },
  { key: 'status', label: 'Status', type: 'default' as const },
]

// Helper functions to get names by IDs
const getCampaignName = (campaignId: number | null): string => {
  if (campaignId === null) return 'All Campaigns'
  const campaign = props.campaigns.find(camp => camp.id === campaignId)
  return campaign ? campaign.name : `Unknown Campaign (ID: ${campaignId})`
}

const getUserName = (userId: number | null): string => {
  if (userId === null) return 'All Users'
  const user = props.users.find(u => u.id === userId)
  return user ? user.username : `Unknown User (ID: ${userId})`
}

// Modal functions
const openCreateModal = () => {
  isEditing.value = false
  editingApplication.value = null
  resetForm()
  applicationModal.value?.showModal()
}

const openEditModal = (application: Application) => {
  isEditing.value = true
  editingApplication.value = application
  fillForm(application)
  applicationModal.value?.showModal()
}

const closeModal = () => {
  applicationModal.value?.close()
  resetForm()
}

// Form functions
const resetForm = () => {
  formData.campaign_id = null
  formData.user_id = null
  formData.status = 'pending'
}

const fillForm = (application: Application) => {
  formData.campaign_id = application.campaign_id
  formData.user_id = application.user_id
  formData.status = application.status as ApplicationStatus
}

// Submit handler
const handleSubmit = async () => {
  if (!formData.campaign_id || !formData.user_id || !formData.status) {
    console.error('All fields are required')
    return
  }

  try {
    if (isEditing.value && editingApplication.value) {
      // Update existing application
      const updateData: any = {}
      if (formData.campaign_id) updateData.campaign_id = formData.campaign_id
      if (formData.user_id) updateData.user_id = formData.user_id
      if (formData.status) updateData.status = formData.status

      await updateApplicationMutation.mutateAsync({
        applicationId: editingApplication.value.id,
        applicationData: updateData,
      })
    } else {
      // Create new application
      await createApplicationMutation.mutateAsync({
        campaign_id: formData.campaign_id,
        user_id: formData.user_id,
        status: formData.status as ApplicationStatus,
      })
    }
    
    closeModal()
  } catch (error) {
    console.error('Error saving application:', error)
  }
}

const handleDelete = (application: Application) => {
  emit('delete', application)
}
</script>
