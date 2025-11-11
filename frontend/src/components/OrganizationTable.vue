<template>
  <div class="tab-content">
    <BaseTable
      title="Organizations"
      :data="props.organizations"
      :columns="columns"
      :icon="OfficeBuildingIcon"
      add-button-text="Add Organization"
      border-class="border-secondary"
      icon-bg-class="bg-secondary/10"
      icon-color-class="text-secondary"
      button-class="btn-secondary"
      @add="openCreateModal"
      @edit="openEditModal"
      @delete="handleDelete"
    />
  </div>

  <!-- Create/Edit Modal -->
  <dialog ref="organizationModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ isEditing ? 'Edit Organization' : 'Create New Organization' }}
      </h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-4 mt-4">
        <!-- Name field -->
        <div>
          <label class="label">
            <span class="label-text">Name</span>
          </label>
          <input
            v-model="formData.name"
            type="text"
            class="input input-bordered w-full"
            placeholder="Enter organization name"
            required
          />
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
            class="btn btn-secondary"
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
import { ref, reactive, computed, watch, type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import OfficeBuildingIcon from 'vue-material-design-icons/OfficeBuilding.vue'
import { useCreateOrganizationMutation, useUpdateOrganizationMutation } from '@/hooks/mutations'
import type { Organization, DatabaseType } from '../types'

const props = defineProps({
  organizations: {
    type: Array as PropType<Organization[]>,
    required: true,
  },
  selectedDatabase: {
    type: String as PropType<DatabaseType>,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'delete', organization: Organization): void
}>()

// Database type reactive ref
const dbTypeRef = ref(props.selectedDatabase)

// Watch for database changes
watch(() => props.selectedDatabase, (newDb) => {
  dbTypeRef.value = newDb
})

// Modal refs and state
const organizationModal = ref<HTMLDialogElement>()
const isEditing = ref(false)
const editingOrganization = ref<Organization | null>(null)

// Form data
const formData = reactive({
  name: '',
})

// Mutations
const createOrganizationMutation = useCreateOrganizationMutation(dbTypeRef)
const updateOrganizationMutation = useUpdateOrganizationMutation(dbTypeRef)

// Computed properties
const isSubmitting = computed(() => 
  createOrganizationMutation.isPending.value || updateOrganizationMutation.isPending.value
)

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-secondary' },
  { key: 'name', label: 'Name', type: 'text' as const },
]

// Modal functions
const openCreateModal = () => {
  isEditing.value = false
  editingOrganization.value = null
  resetForm()
  organizationModal.value?.showModal()
}

const openEditModal = (organization: Organization) => {
  isEditing.value = true
  editingOrganization.value = organization
  fillForm(organization)
  organizationModal.value?.showModal()
}

const closeModal = () => {
  organizationModal.value?.close()
  resetForm()
}

// Form functions
const resetForm = () => {
  formData.name = ''
}

const fillForm = (organization: Organization) => {
  formData.name = organization.name
}

// Submit handler
const handleSubmit = async () => {
  try {
    if (isEditing.value && editingOrganization.value) {
      // Update existing organization
      const updateData: any = {}
      if (formData.name) updateData.name = formData.name

      await updateOrganizationMutation.mutateAsync({
        organizationId: editingOrganization.value.id,
        organizationData: updateData,
      })
    } else {
      // Create new organization
      await createOrganizationMutation.mutateAsync({
        name: formData.name,
      })
    }
    
    closeModal()
  } catch (error) {
    console.error('Error saving organization:', error)
    // You could add toast notification here
  }
}

const handleDelete = (organization: Organization) => {
  emit('delete', organization)
}
</script>
