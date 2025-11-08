<template>
  <div class="tab-content bg-base-100 rounded-box p-6 shadow-lg" :class="borderClass">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-base-content flex items-center gap-2">
        <div class="p-2 rounded-lg" :class="iconBgClass">
          <component :is="icon" class="w-6 h-6" :class="iconColorClass" />
        </div>
        {{ title }}
      </h2>
      <button class="btn shadow-lg" :class="buttonClass" @click="$emit('add')">
        <PlusIcon />
        {{ addButtonText }}
      </button>
    </div>
    
    <div class="overflow-x-auto">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key" class="text-base-content">
              {{ column.label }}
            </th>
            <th class="text-base-content">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedData" :key="item.id">
            <td v-for="column in columns" :key="column.key">
              <slot :name="`cell-${column.key}`" :item="item" :value="item[column.key]">
                <span v-if="column.type === 'badge'" class="badge badge-outline" :class="column.badgeClass || 'badge-primary'">
                  {{ item[column.key] }}
                </span>
                <span v-else-if="column.type === 'text'" class="font-semibold text-base-content">
                  {{ item[column.key] }}
                </span>
                <span v-else-if="column.type === 'accent'" :class="column.accentClass || 'text-primary'">
                  {{ item[column.key] }}
                </span>
                <span v-else class="text-base-content">
                  {{ item[column.key] }}
                </span>
              </slot>
            </td>
            <td>
              <div class="flex gap-2">
                <button class="btn btn-sm btn-secondary btn-outline" @click="$emit('edit', item)">
                  <Pencil :className="'w-4 h-4'" />
                  Edit
                </button>
                <button class="btn btn-sm btn-error btn-outline" @click="$emit('delete', item)">
                  <DeleteIcon :className="'w-4 h-4'" />
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center mt-6">
      <div class="join">
        <button 
          class="join-item btn" 
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
        >
          «
        </button>
        <button class="join-item btn">
          Page {{ currentPage }} of {{ totalPages }}
        </button>
        <button 
          class="join-item btn" 
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
        >
          »
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type PropType, computed, ref } from 'vue'
import PlusIcon from 'vue-material-design-icons/Plus.vue'
import Pencil from 'vue-material-design-icons/Pencil.vue'
import DeleteIcon from 'vue-material-design-icons/Delete.vue'
import type { TableColumn } from '../types'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  data: {
    type: Array as PropType<any[]>,
    required: true,
  },
  columns: {
    type: Array as PropType<TableColumn[]>,
    required: true,
  },
  icon: {
    type: Object,
    required: true,
  },
  addButtonText: {
    type: String,
    required: true,
  },
  borderClass: {
    type: String,
    default: 'border-primary',
  },
  iconBgClass: {
    type: String,
    default: 'bg-primary/10',
  },
  iconColorClass: {
    type: String,
    default: 'text-primary',
  },
  buttonClass: {
    type: String,
    default: 'btn-primary',
  },
  itemsPerPage: {
    type: Number,
    default: 5,
  },
})

const emit = defineEmits<{
  (e: 'add'): void
  (e: 'edit', item: any): void
  (e: 'delete', item: any): void
}>()

// Pagination state
const currentPage = ref(1)

// Computed properties for pagination
const totalPages = computed(() => Math.ceil(props.data.length / props.itemsPerPage))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return props.data.slice(start, end)
})

// Pagination methods
const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

// Watch for data changes to reset pagination
import { watch } from 'vue'
watch(() => props.data.length, () => {
  if (currentPage.value > totalPages.value && totalPages.value > 0) {
    currentPage.value = totalPages.value
  }
})
</script>
