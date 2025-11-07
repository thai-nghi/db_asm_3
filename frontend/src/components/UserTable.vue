<template>
  <BaseTable
    title="Users"
    :data="users"
    :columns="columns"
    :icon="People"
    add-button-text="Add User"
    border-class="border-primary"
    icon-bg-class="bg-primary/10"
    icon-color-class="text-primary"
    button-class="btn-primary"
    @add="handleAdd"
    @edit="handleEdit"
    @delete="handleDelete"
  >
    <template #cell-email="{ value }">
      <span class="text-primary">{{ value }}</span>
    </template>
  </BaseTable>
</template>

<script setup lang="ts">
import { PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import People from '@mui/icons-material/People'

interface User {
  id: number
  username: string
  email: string
}

const props = defineProps({
  users: {
    type: Array as PropType<User[]>,
    required: true,
  },
  selectedDatabase: {
    type: String,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'add'): void
  (e: 'edit', user: User): void
  (e: 'delete', user: User): void
}>()

const columns = [
  { key: 'id', label: 'ID', type: 'badge', badgeClass: 'badge-primary' },
  { key: 'username', label: 'Username', type: 'text' },
  { key: 'email', label: 'Email', type: 'accent', accentClass: 'text-primary' },
]

const handleAdd = () => {
  emit('add')
}

const handleEdit = (user: User) => {
  emit('edit', user)
}

const handleDelete = (user: User) => {
  emit('delete', user)
}
</script>
