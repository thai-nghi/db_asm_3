<template>
  <BaseTable
    title="Organizations"
    :data="organizations"
    :columns="columns"
    :icon="OfficeBuildingIcon"
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
import { type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import OfficeBuildingIcon from 'vue-material-design-icons/OfficeBuilding.vue'
import type { Organization } from '../types'

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
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-secondary' },
  { key: 'name', label: 'Name', type: 'text' as const },
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
