<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import Button from 'primevue/button'
import { ref, watch } from 'vue'

const reader = new FileReader()

const props = defineProps<{
  modelValue: File | null
}>()

const emit = defineEmits<(e: 'update:modelValue', file: File | null) => void>()

defineExpose<{
  result: string
}>()

const input = ref<HTMLInputElement>()

const result = ref<string>()

const isDragging = ref<boolean>(false)

const handleFileChange = function (event: Event) {
  let target = event.target as HTMLInputElement
  emit('update:modelValue', target.files?.[0] ?? null)
}

watch(
  () => props.modelValue,
  () => {
    if (props.modelValue) {
      if (reader.LOADING) {
        reader.abort()
      }
      reader.onload = function (e) {
        if (e.target && typeof e.target.result === 'string') {
          result.value = e.target.result
        }
      }
      reader.readAsDataURL(props.modelValue)
    }
  }
)

const onBrowse = function () {
  if (!input.value) return
  input.value?.click()
}

const dragover = function (e: Event) {
  e.preventDefault()
  isDragging.value = true
}

const dragleave = function () {
  isDragging.value = false
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div
      :class="[
        'relative flex justify-center overflow-hidden rounded-lg border',
        isDragging ? 'border-primary' : 'border-medium-emphasis'
      ]"
      @dragover="dragover"
      @dragleave="dragleave"
      @drop="dragleave"
    >
      <input
        ref="input"
        type="file"
        accept="image/*"
        class="absolute bottom-0 left-0 right-0 top-0 w-full opacity-0"
        @change="handleFileChange"
      />
      <div class="grow self-stretch py-16">
        <div
          :class="[
            'flex h-64 flex-col items-center justify-center gap-2',
            isDragging ? 'text-primary' : 'text-medium-emphasis'
          ]"
        >
          <template v-if="result">
            <img :src="result" alt="uploaded" class="max-h-48 max-w-64" />
            <span class="text-center">
              {{ isDragging ? $t('release_to_replace_upload') : $t('drag_drop_replace_upload') }}
            </span>
          </template>
          <template v-else>
            <BaseIcon icon="photo" :stroke-width="0.5" class="!h-16 !w-16" />
            <span class="text-center">
              {{ isDragging ? $t('release_to_upload') : $t('drag_drop_upload') }}
            </span>
          </template>
        </div>
      </div>
    </div>
    <Button outlined rounded :label="$t('browse')" class="max-sm:w-full" @click="onBrowse">
      <template #icon>
        <BaseIcon icon="arrow-up-tray" :size="5" :strokeWidth="1.25" />
      </template>
    </Button>
  </div>
</template>
