<template>
  <BaseTable
    title="Campaigns"
    :data="campaigns"
    :columns="columns"
    :icon="Bullhorn"
    add-button-text="Add Campaign"
    border-class="border-accent"
    icon-bg-class="bg-accent/10"
    icon-color-class="text-accent"
    button-class="btn-accent"
    @add="handleAdd"
    @edit="handleEdit"
    @delete="handleDelete"
  >
    <template #cell-organizer_id="{ value }">
      <span class="text-accent font-medium">{{ getOrganizationName(value) }}</span>
    </template>
  </BaseTable>
</template>

<script setup lang="ts">
import { type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import Bullhorn from 'vue-material-design-icons/Bullhorn.vue'
import type { CampaignData, Organization } from '../types'

const props = defineProps({
  campaigns: {
    type: Array as PropType<CampaignData[]>,
    required: true,
  },
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
  (e: 'edit', campaign: CampaignData): void
  (e: 'delete', campaign: CampaignData): void
}>()

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-accent' },
  { key: 'name', label: 'Name', type: 'text' as const },
  { key: 'organizer_id', label: 'Organization', type: 'accent' as const, accentClass: 'text-accent' },
]

// Helper function to get organization name by ID
const getOrganizationName = (organizerId: number): string => {
  const organization = props.organizations.find(org => org.id === organizerId)
  return organization ? organization.name : `Unknown (ID: ${organizerId})`
}

const handleAdd = () => {
  emit('add')
}

const handleEdit = (campaign: CampaignData) => {
  emit('edit', campaign)
}

const handleDelete = (campaign: CampaignData) => {
  emit('delete', campaign)
}
</script>
