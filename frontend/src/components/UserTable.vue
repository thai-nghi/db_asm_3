<template>
  <div class="tab-content bg-base-100 border-base-300 rounded-box p-6">
    <BaseTable
      title="Users"
      :data="props.users"
      :columns="columns"
      :icon="AccountGroup"
      add-button-text="Add User"
      border-class="border-primary"
      icon-bg-class="bg-primary/10"
      icon-color-class="text-primary"
      button-class="btn-primary"
      @add="openCreateModal"
      @edit="openEditModal"
      @delete="handleDelete"
    >
      <template #cell-email="{ value }">
        <span class="text-primary">{{ value }}</span>
      </template>
    </BaseTable>
  </div>

  <!-- Create/Edit Modal -->
  <dialog ref="userModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ isEditing ? 'Edit User' : 'Create New User' }}
      </h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-4 mt-4">
        <!-- Username field -->
        <div>
          <label class="label">
            <span class="label-text">Username</span>
          </label>
          <input
            v-model="formData.username"
            type="text"
            class="input input-bordered w-full"
            placeholder="Enter username"
            :required="!isEditing"
          />
        </div>

        <!-- Email field -->
        <div>
          <label class="label">
            <span class="label-text">Email</span>
          </label>
          <input
            v-model="formData.email"
            type="email"
            class="input input-bordered w-full"
            placeholder="Enter email"
            :required="!isEditing"
          />
        </div>

        <!-- Password field -->
        <div>
          <label class="label">
            <span class="label-text">
              {{ isEditing ? 'New Password (optional)' : 'Password' }}
            </span>
          </label>
          <input
            v-model="formData.password"
            type="password"
            class="input input-bordered w-full"
            placeholder="Enter password"
            :required="!isEditing"
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
            class="btn btn-primary"
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
import AccountGroup from 'vue-material-design-icons/AccountGroup.vue'
import { useCreateUserMutation, useUpdateUserMutation } from '@/hooks/mutations'
import type { User, DatabaseType } from '../types'

const props = defineProps({
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
  (e: 'delete', user: User): void
}>()

// Reactive database ref for mutations
const dbTypeRef = ref(props.selectedDatabase)

// Watch for database changes to update mutation refs
watch(() => props.selectedDatabase, (newDb) => {
  dbTypeRef.value = newDb
})

// Modal refs and state
const userModal = ref<HTMLDialogElement>()
const isEditing = ref(false)
const editingUser = ref<User | null>(null)

// Form data
const formData = reactive({
  username: '',
  email: '',
  password: '',
})

// Mutations with reactive database ref
const createUserMutation = useCreateUserMutation(dbTypeRef)
const updateUserMutation = useUpdateUserMutation(dbTypeRef)

// Computed properties
const isSubmitting = computed(() => 
  createUserMutation.isPending.value || updateUserMutation.isPending.value
)

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-primary' },
  { key: 'username', label: 'Username', type: 'text' as const },
  { key: 'email', label: 'Email', type: 'accent' as const, accentClass: 'text-primary' },
]

// Modal functions
const openCreateModal = () => {
  isEditing.value = false
  editingUser.value = null
  resetForm()
  userModal.value?.showModal()
}

const openEditModal = (user: User) => {
  isEditing.value = true
  editingUser.value = user
  fillForm(user)
  userModal.value?.showModal()
}

const closeModal = () => {
  userModal.value?.close()
  resetForm()
}

// Form functions
const resetForm = () => {
  formData.username = ''
  formData.email = ''
  formData.password = ''
}

const fillForm = (user: User) => {
  formData.username = user.username
  formData.email = user.email
  formData.password = '' // Don't pre-fill password for security
}

// Submit handler
const handleSubmit = async () => {
  try {
    if (isEditing.value && editingUser.value) {
      // Update existing user
      const updateData: any = {}
      if (formData.username) updateData.username = formData.username
      if (formData.email) updateData.email = formData.email
      if (formData.password) updateData.password = formData.password

      await updateUserMutation.mutateAsync({
        userId: editingUser.value.id,
        userData: updateData,
      })
    } else {
      // Create new user
      await createUserMutation.mutateAsync({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      })
    }
    
    closeModal()
  } catch (error) {
    console.error('Error saving user:', error)
    // You could add toast notification here
  }
}

const handleDelete = (user: User) => {
  emit('delete', user)
}
</script>
