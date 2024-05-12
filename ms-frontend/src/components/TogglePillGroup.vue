<script setup lang="ts">
import TogglePill from '@/components/TogglePill.vue'

const props = withDefaults(
  defineProps<{
    modelValue: string[]
    options?: string[]
  }>(),
  {
    options: () => []
  }
)

const emit = defineEmits<(e: 'update:modelValue', value: string[]) => void>()

const onSelectOption = function (option: string) {
  const index = props.modelValue.indexOf(option)
  const modelValueCopy = [...props.modelValue]
  if (index !== -1) {
    modelValueCopy.splice(index, 1)
  } else {
    modelValueCopy.push(option)
  }
  emit('update:modelValue', modelValueCopy)
}
</script>

<template>
  <div class="align-start flex flex-wrap gap-2">
    <TogglePill
      v-for="option in options"
      :labelKey="option"
      :active="modelValue.includes(option)"
      :key="option"
      @click="() => onSelectOption(option)"
      @keyup.space="() => onSelectOption(option)"
    />
  </div>
</template>
