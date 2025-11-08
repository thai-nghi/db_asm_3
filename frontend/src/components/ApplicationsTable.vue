<template>
  <BaseTable
    title="Applications"
    :data="applications"
    :columns="columns"
    :icon="FileDocumentIcon"
    add-button-text="Add Application"
    border-class="border-neutral"
    icon-bg-class="bg-neutral/10"
    icon-color-class="text-neutral"
    button-class="btn-neutral"
    @add="handleAdd"
    @edit="handleEdit"
    @delete="handleDelete"
  >
    <template #cell-campaign_id="{ value }">
      <span class="text-neutral font-medium">{{ getCampaignName(value) }}</span>
    </template>
    <template #cell-user_id="{ value }">
      <span class="text-neutral font-medium">{{ getUserName(value) }}</span>
    </template>
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
import { type PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import FileDocumentIcon from 'vue-material-design-icons/FileDocument.vue'
import type { Application, CampaignData, User } from '../types'

const props = defineProps({
  applications: {
    type: Array as PropType<Application[]>,
    required: true,
  },
  campaigns: {
    type: Array as PropType<CampaignData[]>,
    required: true,
  },
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
  (e: 'edit', application: Application): void
  (e: 'delete', application: Application): void
}>()

const columns = [
  { key: 'id', label: 'ID', type: 'badge' as const, badgeClass: 'badge-neutral' },
  { key: 'campaign_id', label: 'Campaign', type: 'text' as const },
  { key: 'user_id', label: 'User', type: 'text' as const },
  { key: 'status', label: 'Status', type: 'default' as const },
]

// Helper functions to get names by IDs
const getCampaignName = (campaignId: number): string => {
  const campaign = props.campaigns.find(camp => camp.id === campaignId)
  return campaign ? campaign.name : `Unknown Campaign (ID: ${campaignId})`
}

const getUserName = (userId: number): string => {
  const user = props.users.find(u => u.id === userId)
  return user ? user.username : `Unknown User (ID: ${userId})`
}

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
