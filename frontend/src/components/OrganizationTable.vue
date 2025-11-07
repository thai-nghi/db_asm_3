<template>
  <BaseTable
    title="Organizations"
    :data="organizations"
    :columns="columns"
    :icon="Business"
    add-button-text="Add Organization"
    border-class="border-secondary"
    icon-bg-class="bg-secondary/10"
    icon-color-class="text-secondary"
    button-class="btn-secondary"
    @add="handleAdd"
    @edit="handleEdit"
    @delete="handleDelete"
  />
</template>

<script setup lang="ts">
import { PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import Business from '@mui/icons-material/Business'

interface Organization {
  id: number
  name: string
}

const props = defineProps({
  organizations: {
    type: Array as PropType<Organization[]>,
    required: true,
  },
  selectedDatabase: {
    type: String,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'add'): void
  (e: 'edit', organization: Organization): void
  (e: 'delete', organization: Organization): void
}>()

const columns = [
  { key: 'id', label: 'ID', type: 'badge', badgeClass: 'badge-secondary' },
  { key: 'name', label: 'Name', type: 'text' },
]

const handleAdd = () => {
  emit('add')
}

const handleEdit = (organization: Organization) => {
  emit('edit', organization)
}

const handleDelete = (organization: Organization) => {
  emit('delete', organization)
}
</script>
