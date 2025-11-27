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
      @row-click="openEditModal"
    >
      <template #cell-email="{ value }">
        <span class="text-primary">{{ value }}</span>
      </template>
    </BaseTable>
  </div>

  <!-- Unified User Modal -->
  <dialog ref="userModal" class="modal">
    <div class="modal-box w-11/12 max-w-3xl">
      <h3 class="text-lg font-bold mb-4">
        {{ isEditing ? 'Edit User' : 'Create New User' }}
      </h3>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Basic Information Section -->
        <div class="card bg-base-200 shadow-sm">
          <div class="card-body p-4">
            <h4 class="card-title text-sm uppercase text-primary mb-2">Basic Information</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
              <div class="md:col-span-2">
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
            </div>
          </div>
        </div>

        <!-- Extended Information (Only for Edit Mode) -->
        <template v-if="isEditing && editingUser">
          <!-- Country Section -->
          <div class="card bg-base-200 shadow-sm">
            <div class="card-body p-4">
              <h4 class="card-title text-sm uppercase text-secondary mb-2">Country</h4>
              <div class="form-control">
                <select 
                  v-model.number="countryForm.countryId" 
                  class="select select-bordered w-full"
                >
                  <option :value="0">Select a country</option>
                  <option 
                    v-for="country in countriesQuery.data.value" 
                    :key="country.id" 
                    :value="country.id"
                  >
                    {{ country.code }} (ID: {{ country.id }})
                  </option>
                </select>
                <div class="label">
                  <span class="label-text-alt text-info" v-if="countryForm.isDirty">
                    Click "Update" at the bottom to save country changes.
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Accounts Section -->
          <div class="card bg-base-200 shadow-sm">
            <div class="card-body p-4">
              <div class="flex justify-between items-center mb-3">
                <h4 class="card-title text-sm uppercase text-accent">Social Media Accounts</h4>
                <button 
                  type="button"
                  class="btn btn-xs btn-accent btn-outline"
                  @click="openAccountCreateModal"
                >
                  Add Account
                </button>
              </div>

              <div v-if="userAccountsQuery.isPending.value" class="loading loading-spinner loading-sm"></div>
              <div v-else-if="userAccountsQuery.data.value && userAccountsQuery.data.value.length > 0">
                <div class="space-y-2">
                  <div 
                    v-for="userAccount in userAccountsQuery.data.value" 
                    :key="userAccount.id"
                    class="flex justify-between items-center p-2 bg-base-100 rounded-lg border border-base-300"
                  >
                    <div class="text-sm">
                      <div class="font-medium flex items-center gap-2">
                        <span class="text-primary">{{ getAccountDetails(userAccount.account_id)?.username || 'Unknown' }}</span>
                        <span class="badge badge-sm badge-ghost">{{ getAccountDetails(userAccount.account_id)?.followers || 0 }} followers</span>
                      </div>
                      <div class="text-xs opacity-50">ID: {{ userAccount.account_id }}</div>
                    </div>
                    <button 
                      type="button"
                      class="btn btn-xs btn-ghost text-accent"
                      @click="openAccountEditModal(userAccount)"
                    >
                      Edit
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="text-sm text-gray-500 italic">
                No accounts linked.
              </div>
            </div>
          </div>
        </template>

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
            {{ isEditing ? 'Update User' : 'Create User' }}
          </button>
        </div>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button type="button" @click="closeModal">close</button>
    </form>
  </dialog>

  <!-- Account Create/Edit Modal (Sub-modal) -->
  <dialog ref="accountModal" class="modal">
    <div class="modal-box">
      <h3 class="text-lg font-bold">
        {{ editingUserAccount ? 'Edit Account Link' : 'Create & Link New Account' }}
      </h3>
      
      <form @submit.prevent="handleAccountSubmit" class="space-y-4 mt-4">
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
import { ref, reactive, computed, type PropType, watch } from 'vue'
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
import { useUserCountryQuery, useUserAccountsQuery, useCountriesQuery, useAccountsQuery } from '@/hooks/queries'
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

// Modal refs
const userModal = ref<HTMLDialogElement>()
const accountModal = ref<HTMLDialogElement>()

// State
const isEditing = ref(false)
const editingUser = ref<UserResponse | null>(null)
const editingUserAccount = ref<UserAccountResponse | null>(null)

// Form data
const formData = reactive({
  username: '',
  email: '',
  password: '',
})

const countryForm = reactive({
  countryId: 0,
  isDirty: false,
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

// Queries
const selectedUserId = computed(() => editingUser.value?.id ?? 0)
const countriesQuery = useCountriesQuery()
const accountsQuery = useAccountsQuery()

const userCountryQuery = useUserCountryQuery(
  selectedUserId,
  computed(() => isEditing.value && !!editingUser.value)
)

const userAccountsQuery = useUserAccountsQuery(
  selectedUserId,
  computed(() => isEditing.value && !!editingUser.value)
)

// Helper to get account details
const getAccountDetails = (accountId: string) => {
  return accountsQuery.data.value?.find(a => a.id === accountId)
}

// Watchers to populate country form when data loads
watch(() => userCountryQuery.data.value, (newCountry) => {
  if (newCountry) {
    countryForm.countryId = newCountry.id
  } else {
    countryForm.countryId = 0
  }
  countryForm.isDirty = false
})

watch(() => countryForm.countryId, () => {
  countryForm.isDirty = true
})

// Computed properties
const isSubmitting = computed(() => 
  createUserMutation.isPending.value || 
  updateUserMutation.isPending.value ||
  setCountryMutation.isPending.value
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

// Modal functions
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
  countryForm.countryId = 0
  countryForm.isDirty = false
}

const fillForm = (user: UserResponse) => {
  formData.username = user.username
  formData.email = user.email
  formData.password = ''
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

      // Update country if changed
      if (countryForm.isDirty) {
        await setCountryMutation.mutateAsync({
          userId: editingUser.value.id,
          countryId: countryForm.countryId,
        })
      }
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

const handleAccountSubmit = async () => {
  if (!editingUser.value) return
  
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
        user_id: editingUser.value.id,
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
