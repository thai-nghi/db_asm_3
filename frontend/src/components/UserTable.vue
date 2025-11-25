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
      @row-click="openDetailModal"
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

  <!-- User Detail Modal -->
  <dialog ref="detailModal" class="modal">
    <div class="modal-box w-11/12 max-w-2xl">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xl font-bold">User Details</h3>
        <button 
          class="btn btn-sm btn-circle btn-ghost"
          @click="closeDetailModal"
        >
          ✕
        </button>
      </div>

      <div v-if="selectedUser" class="space-y-6">
        <!-- Basic User Information -->
        <div class="card bg-base-200 shadow-sm">
          <div class="card-body p-4">
            <h4 class="card-title text-primary">Basic Information</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <span class="text-sm opacity-70">ID:</span>
                <div class="badge badge-primary">{{ selectedUser.id }}</div>
              </div>
              <div>
                <span class="text-sm opacity-70">Username:</span>
                <div class="font-medium">{{ selectedUser.username }}</div>
              </div>
              <div class="sm:col-span-2">
                <span class="text-sm opacity-70">Email:</span>
                <div class="text-primary">{{ selectedUser.email }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Country Information -->
        <div class="card bg-base-200 shadow-sm">
          <div class="card-body p-4">
            <div class="flex justify-between items-center mb-3">
              <h4 class="card-title text-secondary">Country</h4>
              <button 
                class="btn btn-sm btn-secondary btn-outline"
                @click="openCountryEditModal"
              >
                Edit Country
              </button>
            </div>
            
            <div v-if="userCountryQuery.isPending.value" class="loading loading-spinner loading-sm"></div>
            <div v-else-if="userCountryQuery.error.value" class="text-error">
              Failed to load country information
            </div>
            <div v-else-if="userCountryQuery.data.value" class="flex items-center gap-2">
              <span class="badge badge-secondary">{{ userCountryQuery.data.value.code }}</span>
              <span>Country ID: {{ userCountryQuery.data.value.id }}</span>
            </div>
            <div v-else class="flex items-center gap-2">
              <span class="text-gray-500 italic">No country set</span>
              <span class="text-xs opacity-50">(Click "Edit Country" to set one)</span>
            </div>
          </div>
        </div>

        <!-- User Accounts -->
        <div class="card bg-base-200 shadow-sm">
          <div class="card-body p-4">
            <div class="flex justify-between items-center mb-3">
              <h4 class="card-title text-accent">Social Media Accounts</h4>
              <button 
                class="btn btn-sm btn-accent btn-outline"
                @click="openAccountCreateModal"
              >
                Add Account
              </button>
            </div>

            <div v-if="userAccountsQuery.isPending.value" class="loading loading-spinner loading-sm"></div>
            <div v-else-if="userAccountsQuery.error.value" class="text-error">
              Failed to load accounts
            </div>
            <div v-else-if="userAccountsQuery.data.value && userAccountsQuery.data.value.length > 0">
              <div class="space-y-3">
                <div 
                  v-for="userAccount in userAccountsQuery.data.value" 
                  :key="userAccount.id"
                  class="flex justify-between items-center p-3 bg-base-100 rounded-lg"
                >
                  <div>
                    <div class="font-medium">Account: {{ userAccount.account_id }}</div>
                    <div class="text-sm opacity-70">User Account ID: {{ userAccount.id }}</div>
                  </div>
                  <button 
                    class="btn btn-sm btn-ghost text-accent"
                    @click="openAccountEditModal(userAccount)"
                  >
                    Edit
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="flex items-center gap-2">
              <span class="text-gray-500 italic">No accounts linked</span>
              <span class="text-xs opacity-50">(Click "Add Account" to link one)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button type="button" @click="closeDetailModal">close</button>
    </form>
  </dialog>

  <!-- Country Edit Modal -->
  <dialog ref="countryModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">Update User Country</h3>
      
      <form @submit.prevent="handleCountrySubmit" class="space-y-4 mt-4">
        <div>
          <label class="label">
            <span class="label-text">Country</span>
          </label>
          <select 
            v-model.number="countryForm.countryId" 
            class="select select-bordered w-full"
            required
          >
            <option disabled value="0">Select a country</option>
            <option 
              v-for="country in countriesQuery.data.value" 
              :key="country.id" 
              :value="country.id"
            >
              {{ country.code }} (ID: {{ country.id }})
            </option>
          </select>
        </div>

        <div class="modal-action">
          <button
            type="button"
            class="btn btn-ghost"
            @click="closeCountryModal"
            :disabled="setCountryMutation.isPending.value"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn btn-secondary"
            :disabled="setCountryMutation.isPending.value"
          >
            <span v-if="setCountryMutation.isPending.value" class="loading loading-spinner loading-sm"></span>
            Update Country
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button type="button" @click="closeCountryModal">close</button>
    </form>
  </dialog>

  <!-- Account Create/Edit Modal -->
  <dialog ref="accountModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ editingUserAccount ? 'Edit Account Link' : 'Create & Link New Account' }}
      </h3>
      
      <form @submit.prevent="handleAccountSubmit" class="space-y-4 mt-4">
        <!-- Create new account fields -->
        <template v-if="!editingUserAccount">
          <div>
            <label class="label">
              <span class="label-text">Username</span>
            </label>
            <input
              v-model="accountForm.username"
              type="text"
              class="input input-bordered w-full"
              placeholder="Enter account username"
              required
            />
          </div>
          
          <div>
            <label class="label">
              <span class="label-text">Followers</span>
            </label>
            <input
              v-model.number="accountForm.followers"
              type="number"
              class="input input-bordered w-full"
              placeholder="Enter number of followers"
              required
            />
          </div>
        </template>

        <!-- Edit existing link (only allows changing account ID if needed, but usually we might want to edit the account itself? 
             The requirement says "add a new account", so for edit we might keep it simple or just allow relinking. 
             Let's assume for edit we still just link by ID or maybe we shouldn't allow editing link this way?
             The original code allowed editing the account_id in the link. 
             Let's keep the original behavior for EDIT, but change for CREATE.
        -->
        <div v-else>
          <label class="label">
            <span class="label-text">Account ID</span>
          </label>
          <input
            v-model="accountForm.accountId"
            type="text"
            class="input input-bordered w-full"
            placeholder="Enter account ID"
            required
          />
        </div>

        <div class="modal-action">
          <button
            type="button"
            class="btn btn-ghost"
            @click="closeAccountModal"
            :disabled="accountSubmitting"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="btn btn-accent"
            :disabled="accountSubmitting"
          >
            <span v-if="accountSubmitting" class="loading loading-spinner loading-sm"></span>
            {{ editingUserAccount ? 'Update Link' : 'Create & Link' }}
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button type="button" @click="closeAccountModal">close</button>
    </form>
  </dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import AccountGroup from 'vue-material-design-icons/AccountGroup.vue'
import { 
  useCreateUserMutation, 
  useUpdateUserMutation, 
  useSetUserCountryMutation,
  useCreateUserAccountMutation,
  useUpdateUserAccountMutation,
  useCreateAccountMutation
} from '@/hooks/mutations'
import { useUserCountryQuery, useUserAccountsQuery, useCountriesQuery } from '@/hooks/queries'
import type { UserResponse, UserAccountResponse } from '@/api'

const props = defineProps({
  users: {
    type: Array as PropType<UserResponse[]>,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'delete', user: UserResponse): void
}>()

// Modal refs and state
const userModal = ref<HTMLDialogElement>()
const detailModal = ref<HTMLDialogElement>()
const countryModal = ref<HTMLDialogElement>()
const accountModal = ref<HTMLDialogElement>()

const isEditing = ref(false)
const editingUser = ref<UserResponse | null>(null)
const selectedUser = ref<UserResponse | null>(null)
const editingUserAccount = ref<UserAccountResponse | null>(null)

// Form data
const formData = reactive({
  username: '',
  email: '',
  password: '',
})

const countryForm = reactive({
  countryId: 0,
})

const accountForm = reactive({
  accountId: '',
  username: '',
  followers: 0,
})

// Mutations
const createUserMutation = useCreateUserMutation()
const updateUserMutation = useUpdateUserMutation()
const setCountryMutation = useSetUserCountryMutation()
const createUserAccountMutation = useCreateUserAccountMutation()
const updateUserAccountMutation = useUpdateUserAccountMutation()
const createAccountMutation = useCreateAccountMutation()

// Computed properties for selected user queries
const selectedUserId = computed(() => selectedUser.value?.id ?? 0)

const countriesQuery = useCountriesQuery()

// Conditional queries - only run when user is selected
const userCountryQuery = useUserCountryQuery(
  selectedUserId,
  computed(() => !!selectedUser.value)
)

const userAccountsQuery = useUserAccountsQuery(
  selectedUserId,
  computed(() => !!selectedUser.value)
)

// Computed properties
const isSubmitting = computed(() => 
  createUserMutation.isPending.value || updateUserMutation.isPending.value
)

const accountSubmitting = computed(() =>
  createUserAccountMutation.isPending.value || 
  updateUserAccountMutation.isPending.value ||
  createAccountMutation.isPending.value
)

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-primary' },
  { key: 'username', label: 'Username', type: 'text' as const },
  { key: 'email', label: 'Email', type: 'accent' as const, accentClass: 'text-primary' },
]

// Modal functions for user CRUD
const openCreateModal = () => {
  isEditing.value = false
  editingUser.value = null
  resetForm()
  userModal.value?.showModal()
}

const openEditModal = (user: UserResponse) => {
  isEditing.value = true
  editingUser.value = user
  fillForm(user)
  userModal.value?.showModal()
}

const closeModal = () => {
  userModal.value?.close()
  resetForm()
}

// Detail modal functions
const openDetailModal = (user: UserResponse) => {
  selectedUser.value = user
  detailModal.value?.showModal()
}

const closeDetailModal = () => {
  selectedUser.value = null
  detailModal.value?.close()
}

// Country modal functions
const openCountryEditModal = () => {
  if (selectedUser.value && userCountryQuery.data.value) {
    countryForm.countryId = userCountryQuery.data.value.id
  } else {
    countryForm.countryId = 0
  }
  countryModal.value?.showModal()
}

const closeCountryModal = () => {
  countryForm.countryId = 0
  countryModal.value?.close()
}

// Account modal functions
const openAccountCreateModal = () => {
  editingUserAccount.value = null
  accountForm.accountId = ''
  accountForm.username = ''
  accountForm.followers = 0
  accountModal.value?.showModal()
}

const openAccountEditModal = (userAccount: UserAccountResponse) => {
  editingUserAccount.value = userAccount
  accountForm.accountId = userAccount.account_id
  accountModal.value?.showModal()
}

const closeAccountModal = () => {
  editingUserAccount.value = null
  accountForm.accountId = ''
  accountModal.value?.close()
}

// Form functions
const resetForm = () => {
  formData.username = ''
  formData.email = ''
  formData.password = ''
}

const fillForm = (user: UserResponse) => {
  formData.username = user.username
  formData.email = user.email
  formData.password = '' // Don't pre-fill password for security
}

// Submit handlers
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
  }
}

const handleCountrySubmit = async () => {
  if (!selectedUser.value) return
  
  try {
    await setCountryMutation.mutateAsync({
      userId: selectedUser.value.id,
      countryId: countryForm.countryId,
    })
    closeCountryModal()
  } catch (error) {
    console.error('Error updating country:', error)
  }
}

const handleAccountSubmit = async () => {
  if (!selectedUser.value) return
  
  try {
    if (editingUserAccount.value) {
      // Update existing user account
      await updateUserAccountMutation.mutateAsync({
        userAccountId: editingUserAccount.value.id,
        userAccountData: {
          account_id: accountForm.accountId,
        },
      })
    } else {
      // Create new account first
      const newAccount = await createAccountMutation.mutateAsync({
        username: accountForm.username,
        followers: accountForm.followers,
      })
      
      // Then link it to the user
      await createUserAccountMutation.mutateAsync({
        user_id: selectedUser.value.id,
        account_id: newAccount.id,
      })
    }
    closeAccountModal()
  } catch (error) {
    console.error('Error saving account:', error)
  }
}

const handleDelete = (user: UserResponse) => {
  emit('delete', user)
}
</script>
