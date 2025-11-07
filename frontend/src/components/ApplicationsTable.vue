<template>
  <BaseTable
    title="Applications"
    :data="applications"
    :columns="columns"
    :icon="Description"
    add-button-text="Add Application"
    border-class="border-neutral"
    icon-bg-class="bg-neutral/10"
    icon-color-class="text-neutral"
    button-class="btn-neutral"
    @add="handleAdd"
    @edit="handleEdit"
    @delete="handleDelete"
  >
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
</template>

<script setup lang="ts">
import { PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import Description from '@mui/icons-material/Description'

interface Application {
  id: number
  campaign_id: number
  user_id: number
  status: 'PENDING' | 'APPROVED' | 'REJECTED'
}

const props = defineProps({
  applications: {
    type: Array as PropType<Application[]>,
    required: true,
  },
  selectedDatabase: {
    type: String,
    required: true,
  },
})

const emit = defineEmits<{
  (e: 'add'): void
  (e: 'edit', application: Application): void
  (e: 'delete', application: Application): void
}>()

const columns = [
  { key: 'id', label: 'ID', type: 'badge', badgeClass: 'badge-neutral' },
  { key: 'campaign_id', label: 'Campaign ID', type: 'text' },
  { key: 'user_id', label: 'User ID', type: 'text' },
  { key: 'status', label: 'Status', type: 'default' },
]

const handleAdd = () => {
  emit('add')
}

const handleEdit = (application: Application) => {
  emit('edit', application)
}

const handleDelete = (application: Application) => {
  emit('delete', application)
}
</script>
