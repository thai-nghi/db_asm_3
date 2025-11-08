<template>
  <BaseTable
    title="Users"
    :data="users"
    :columns="columns"
    :icon="AccountGroup"
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
import { type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import AccountGroup from 'vue-material-design-icons/AccountGroup.vue'
import type { User, TableColumn } from '../types'

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
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-primary' },
  { key: 'username', label: 'Username', type: 'text' as const },
  { key: 'email', label: 'Email', type: 'accent' as const, accentClass: 'text-primary' },
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
