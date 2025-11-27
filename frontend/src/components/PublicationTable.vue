<template>
  <div class="tab-content">
    <!-- Filter Section -->
    <div class="mb-4">
      <div class="flex items-center gap-4 flex-wrap">
        <!-- Account Filter -->
        <div class="flex items-center gap-2">
          <label class="text-base-content font-medium">Account:</label>
          <select v-model="selectedAccountId" class="select select-bordered select-neutral w-48">
            <option :value="null">All Accounts</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.username }}
            </option>
          </select>
        </div>
        
        <!-- Active Filter Badges -->
        <div class="flex gap-2">
          <div v-if="selectedAccountId !== null" class="badge badge-outline badge-neutral">
            Account: {{ getAccountName(selectedAccountId) }}
          </div>
        </div>
      
      </div>
    </div>

    <!-- Table -->
    <BaseTable
      title="Publications"
      :data="publicationData"
      :columns="columns"
      :icon="FileDocumentIcon"
      add-button-text="Add Publication"
      border-class="border-neutral"
      icon-bg-class="bg-neutral/10"
      icon-color-class="text-neutral"
      button-class="btn-neutral"
      @add="openCreateModal"
      @edit="openEditModal"
      @delete="handleDelete"
    >
      <template #cell-account_id="{ value }">
        <span class="text-neutral font-medium">{{ getAccountName(value) }}</span>
      </template>
      <template #cell-followers="{ item }">
        <span class="text-neutral">{{ getAccountFollowers(item.account_id) }}</span>
      </template>
      <template #cell-likes="{ item }">
        <span class="text-neutral">{{ item.insights.likes }}</span>
      </template>
      <template #cell-comments="{ item }">
        <span class="text-neutral">{{ item.insights.comments }}</span>
      </template>
    </BaseTable>
  </div>

  <!-- Create/Edit Modal -->
  <dialog ref="publicationModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ isEditing ? 'Edit Publication' : 'Create New Publication' }}
      </h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-4 mt-4">
        <!-- Account field -->
        <div>
          <label class="label">
            <span class="label-text">Account</span>
          </label>
          <select
            v-model="formData.account_id"
            class="select select-bordered w-full"
            required
            :disabled="isEditing"
          >
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.username }}
            </option>
          </select>
        </div>

        <!-- Type field -->
        <div>
          <label class="label">
            <span class="label-text">Type</span>
          </label>
          <select
            v-model="formData.type"
            class="select select-bordered w-full"
            required
          >
            <option value="" disabled>Select a type</option>
            <option value="post">Post</option>
            <option value="reel">Reel</option>
            <option value="story">Story</option>
          </select>
        </div>

        <!-- Insights: Likes -->
        <div>
          <label class="label">
            <span class="label-text">Likes</span>
          </label>
          <input
            v-model.number="formData.likes"
            type="number"
            min="0"
            class="input input-bordered w-full"
            required
          />
        </div>

        <!-- Insights: Comments -->
        <div>
          <label class="label">
            <span class="label-text">Comments</span>
          </label>
          <input
            v-model.number="formData.comments"
            type="number"
            min="0"
            class="input input-bordered w-full"
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
import { ref, computed, reactive, type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import FileDocumentIcon from 'vue-material-design-icons/FileDocument.vue'
import { usePublicationsQuery } from '@/hooks/queries'
import { useCreatePublicationMutation, useUpdatePublicationMutation } from '@/hooks/mutations'
import type { Publication, Account } from '../types'

const props = defineProps({
  accounts: {
    type: Array as PropType<Account[]>,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'delete', publication: Publication): void
}>()

// Filter state
const selectedAccountId = ref<string | null>(null)

// Query publications
const { data: publicationsResult } = usePublicationsQuery(
  selectedAccountId
)

const publicationData = computed(() => publicationsResult.value || [])

// Modal refs and state
const publicationModal = ref<HTMLDialogElement>()
const isEditing = ref(false)
const editingPublication = ref<Publication | null>(null)

// Form data
const formData = reactive({
  account_id: '' as string,
  type: '',
  likes: 0,
  comments: 0,
})

// Mutations
const createPublicationMutation = useCreatePublicationMutation()
const updatePublicationMutation = useUpdatePublicationMutation()

// Computed properties
const isSubmitting = computed(() => 
  createPublicationMutation.isPending.value || updatePublicationMutation.isPending.value
)

const columns = [
  { key: 'account_id', label: 'Account', type: 'text' as const },
  { key: 'followers', label: 'Followers', type: 'default' as const },
  { key: 'type', label: 'Type', type: 'text' as const },
  { key: 'likes', label: 'Likes', type: 'default' as const },
  { key: 'comments', label: 'Comments', type: 'default' as const },
]

// Helper functions to get names by IDs
const getAccountName = (accountId: string | null): string => {
  if (accountId === null) return 'All Accounts'
  const account = props.accounts.find(acc => acc.id === accountId)
  return account ? account.username : `Unknown Account (ID: ${accountId})`
}

const getAccountFollowers = (accountId: string | null): number => {
  if (accountId === null) return 0
  const account = props.accounts.find(acc => acc.id === accountId)
  return account ? account.followers : 0
}

// Modal functions
const openCreateModal = () => {
  isEditing.value = false
  editingPublication.value = null
  resetForm()
  publicationModal.value?.showModal()
}

const openEditModal = (publication: Publication) => {
  isEditing.value = true
  editingPublication.value = publication
  fillForm(publication)
  publicationModal.value?.showModal()
}

const closeModal = () => {
  publicationModal.value?.close()
  resetForm()
}

// Form functions
const resetForm = () => {
  // If filtering by account, default to that account
  formData.account_id = selectedAccountId.value || ''
  formData.type = ''
  formData.likes = 0
  formData.comments = 0
}

const fillForm = (publication: Publication) => {
  formData.account_id = publication.account_id
  formData.type = publication.type
  formData.likes = publication.insights.likes
  formData.comments = publication.insights.comments
}

// Submit handler
const handleSubmit = async () => {
  if (!formData.account_id || !formData.type) {
    console.error('All fields are required')
    return
  }

  try {
    const insights = {
      likes: formData.likes,
      comments: formData.comments
    }

    if (isEditing.value && editingPublication.value) {
      // Update existing publication
      const updateData: any = {}
      if (formData.account_id) updateData.account_id = formData.account_id
      if (formData.type) updateData.type = formData.type
      updateData.insights = insights

      await updatePublicationMutation.mutateAsync({
        publicationId: editingPublication.value.id,
        publicationData: updateData,
      })
    } else {
      // Create new publication
      await createPublicationMutation.mutateAsync({
        account_id: formData.account_id,
        type: formData.type,
        insights: insights
      })
    }
    
    closeModal()
  } catch (error) {
    console.error('Error saving publication:', error)
  }
}

const handleDelete = (publication: Publication) => {
  // Implement delete if needed, but not requested explicitly
  // emit('delete', publication)
  console.log('Delete not implemented yet', publication)
}
</script>
