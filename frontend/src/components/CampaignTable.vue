<template>
  <BaseTable
    title="Campaigns"
    :data="campaigns"
    :columns="columns"
    :icon="Campaign"
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
      <span class="text-accent font-medium">{{ value }}</span>
    </template>
  </BaseTable>
</template>

<script setup lang="ts">
import { PropType } from 'vue'
import BaseTable from './BaseTable.vue'
import Campaign from '@mui/icons-material/Campaign'

interface CampaignData {
  id: number
  organizer_id: number
  name: string
}

const props = defineProps({
  campaigns: {
    type: Array as PropType<CampaignData[]>,
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
  { key: 'id', label: 'ID', type: 'badge', badgeClass: 'badge-accent' },
  { key: 'name', label: 'Name', type: 'text' },
  { key: 'organizer_id', label: 'Organizer ID', type: 'accent', accentClass: 'text-accent' },
]

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
