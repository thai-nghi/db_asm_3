<template>
  <div class="tab-content">
    <!-- Filter Section -->
    <div class="mb-4">
      <div class="flex items-center gap-4">
        <label class="text-base-content font-medium">Filter by Organization:</label>
        <select v-model="selectedOrganizationId" class="select select-bordered select-accent w-64">
          <option :value="null">All Organizations</option>
          <option v-for="org in organizations" :key="org.id" :value="org.id">
            {{ org.name }}
          </option>
        </select>
        <div v-if="selectedOrganizationId !== null" class="badge badge-outline badge-accent">
          {{ getOrganizationName(selectedOrganizationId) }}
        </div>
      </div>
    </div>

    <!-- Table -->
    <BaseTable
      title="Campaigns"
      :data="campaignData"
      :columns="columns"
      :icon="Bullhorn"
      add-button-text="Add Campaign"
      border-class="border-accent"
      icon-bg-class="bg-accent/10"
      icon-color-class="text-accent"
      button-class="btn-accent"
      @add="openCreateModal"
      @edit="openEditModal"
    >
      <template #cell-organizer_id="{ value }">
        <span class="text-accent font-medium">{{ getOrganizationName(value) }}</span>
      </template>
      <template #cell-requirements="{ value }">
        <div class="flex flex-wrap gap-1">
          <div v-for="req in value" :key="req.media_type" class="badge badge-outline badge-sm">
            {{ req.count }} {{ req.media_type }}{{ req.count > 1 ? 's' : '' }}
          </div>
        </div>
      </template>
    </BaseTable>
  </div>

  <!-- Create/Edit Modal -->
  <dialog ref="campaignModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ isEditing ? 'Edit Campaign' : 'Create New Campaign' }}
      </h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-4 mt-4">
        <!-- Name field -->
        <div>
          <label class="label">
            <span class="label-text">Campaign Name</span>
          </label>
          <input
            v-model="formData.name"
            type="text"
            class="input input-bordered w-full"
            placeholder="Enter campaign name"
            required
          />
        </div>

        <!-- Organization field -->
        <div>
          <label class="label">
            <span class="label-text">Organization</span>
          </label>
          <select
            v-model="formData.organizer_id"
            class="select select-bordered w-full"
            required
          >
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <!-- Requirements section -->
        <div>
          <label class="label">
            <span class="label-text">Requirements</span>
          </label>
          <div class="space-y-3">
            <div v-for="(requirement, index) in formData.requirements" :key="index" class="flex gap-2 items-end">
              <div class="flex-1">
                <select
                  v-model="requirement.media_type"
                  class="select select-bordered w-full"
                  required
                >
                  <option value="photo">Photo</option>
                  <option value="video">Video</option>
                </select>
              </div>
              <div class="flex-1">
                <input
                  v-model.number="requirement.count"
                  type="number"
                  min="1"
                  class="input input-bordered w-full"
                  placeholder="Count"
                  required
                />
              </div>
              <button
                type="button"
                class="btn btn-square btn-outline btn-error"
                @click="removeRequirement(index)"
                :disabled="formData.requirements.length === 1"
              >
                ×
              </button>
            </div>
            <button
              type="button"
              class="btn btn-outline btn-accent btn-sm"
              @click="addRequirement"
            >
              + Add Requirement
            </button>
          </div>
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
            class="btn btn-accent"
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
import Bullhorn from 'vue-material-design-icons/Bullhorn.vue'
import { useCreateCampaignMutation, useUpdateCampaignMutation } from '@/hooks/mutations'
import type { CampaignData, Organization, DatabaseType, Requirements, MediaType } from '../types'

const props = defineProps({
  campaigns: {
    type: Array as PropType<CampaignData[]>,
    required: true,
  },
  organizations: {
    type: Array as PropType<Organization[]>,
    required: true,
  },
  selectedDatabase: {
    type: String as PropType<DatabaseType>,
    required: true,
  },
  selectedOrganizationId: {
    type: [Number, null] as PropType<number | null>,
    default: null,
  },
})

const emit = defineEmits<{
  (e: 'delete', campaign: CampaignData): void
  (e: 'update-organization-filter', organizationId: number | null): void
}>()

// Database type reactive ref
const dbTypeRef = ref(props.selectedDatabase)

// Watch for database changes
watch(() => props.selectedDatabase, (newDb) => {
  dbTypeRef.value = newDb
})

// Local filter state that emits changes to parent
const selectedOrganizationId = computed({
  get: () => props.selectedOrganizationId,
  set: (value) => emit('update-organization-filter', value)
})

// Use campaigns from props (no query needed here anymore)
const campaignData = computed(() => props.campaigns || [])

// Modal refs and state
const campaignModal = ref<HTMLDialogElement>()
const isEditing = ref(false)
const editingCampaign = ref<CampaignData | null>(null)

// Form data
const formData = reactive({
  name: '',
  organizer_id: null as number | null,
  requirements: [
    { media_type: 'photo' as MediaType, count: 1 }
  ] as Requirements[]
})

// Mutations
const createCampaignMutation = useCreateCampaignMutation(dbTypeRef)
const updateCampaignMutation = useUpdateCampaignMutation(dbTypeRef)

// Computed properties
const isSubmitting = computed(() => 
  createCampaignMutation.isPending.value || updateCampaignMutation.isPending.value
)

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-accent' },
  { key: 'name', label: 'Name', type: 'text' as const },
  { key: 'organizer_id', label: 'Organization', type: 'accent' as const, accentClass: 'text-accent' },
  { key: 'requirements', label: 'Requirements', type: 'text' as const },
]

// Helper function to get organization name by ID
const getOrganizationName = (organizerId: number | null): string => {
  if (organizerId === null) return 'All Organizations'
  const organization = props.organizations.find(org => org.id === organizerId)
  return organization ? organization.name : `Unknown (ID: ${organizerId})`
}

// Modal functions
const openCreateModal = () => {
  isEditing.value = false
  editingCampaign.value = null
  resetForm()
  campaignModal.value?.showModal()
}

const openEditModal = (campaign: CampaignData) => {
  isEditing.value = true
  editingCampaign.value = campaign
  fillForm(campaign)
  campaignModal.value?.showModal()
}

const closeModal = () => {
  campaignModal.value?.close()
  resetForm()
}

// Form functions
const resetForm = () => {
  formData.name = ''
  formData.organizer_id = null
  formData.requirements = [{ media_type: 'photo', count: 1 }]
}

const fillForm = (campaign: CampaignData) => {
  formData.name = campaign.name
  formData.organizer_id = campaign.organizer_id
  formData.requirements = campaign.requirements.length > 0 ? [...campaign.requirements] : [{ media_type: 'photo', count: 1 }]
}

// Requirements management
const addRequirement = () => {
  formData.requirements.push({ media_type: 'photo', count: 1 })
}

const removeRequirement = (index: number) => {
  if (formData.requirements.length > 1) {
    formData.requirements.splice(index, 1)
  }
}

// Submit handler
const handleSubmit = async () => {
  if (!formData.organizer_id) {
    console.error('Organization is required')
    return
  }

  if (formData.requirements.length === 0) {
    console.error('At least one requirement is needed')
    return
  }

  try {
    if (isEditing.value && editingCampaign.value) {
      // Update existing campaign
      const updateData: any = {}
      if (formData.name) updateData.name = formData.name
      if (formData.organizer_id) updateData.organizer_id = formData.organizer_id
      updateData.requirements = formData.requirements

      await updateCampaignMutation.mutateAsync({
        campaignId: editingCampaign.value.id,
        campaignData: updateData,
      })
    } else {
      // Create new campaign
      await createCampaignMutation.mutateAsync({
        name: formData.name,
        organizer_id: formData.organizer_id,
        requirements: formData.requirements,
      })
    }
    
    closeModal()
    // Campaigns will be automatically refetched due to query invalidation in mutations
  } catch (error) {
    console.error('Error saving campaign:', error)
    // You could add toast notification here
  }
}
</script>
