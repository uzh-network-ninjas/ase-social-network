<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import BaseIcon, { type IconType } from '@/icons/BaseIcon.vue'
import MiniChevronDown from '@/icons/MiniChevronDownIcon.vue'
import { ref } from 'vue'
import Dropdown from 'primevue/dropdown'
import { Locales } from '@/i18n'

const i18n = useI18n()

type LanguageOption = { label: string; value: Locales; icon: IconType }

withDefaults(
  defineProps<{
    plain?: boolean
    showFlag?: boolean
  }>(),
  {
    plain: false,
    showFlag: false
  }
)

const languageOptions: LanguageOption[] = [
  { label: 'Deutsch', value: Locales.DE, icon: 'flag-de' },
  { label: 'English', value: Locales.EN, icon: 'flag-en' }
]
const selectedLanguage = ref<LanguageOption | undefined>(
  languageOptions.find((option) => option.value === i18n.locale.value)
)

const updateSelectedLangauge = function (value: LanguageOption | undefined) {
  if (value) {
    i18n.locale.value = value.value
    localStorage.setItem('selectedLanguage', value.value)
    selectedLanguage.value = value
  }
}
</script>

<template>
  <Dropdown
    :modelValue="selectedLanguage"
    @update:modelValue="updateSelectedLangauge"
    :options="languageOptions"
    :class="{ 'border-none': plain }"
  >
    <template #value="{ value }">
      <div class="flex items-center gap-4">
        <BaseIcon :icon="showFlag ? value.icon : 'globe-alt'" class="h-5 w-5" />
        <span>{{ (value as LanguageOption)?.label }}</span>
      </div>
    </template>
    <template #dropdownicon>
      <MiniChevronDown />
    </template>
    <template #option="{ option }">
      <div class="flex items-center gap-2">
        <BaseIcon :icon="option.icon" class="h-5 w-5" />
        <span>{{ (option as LanguageOption)?.label }}</span>
      </div>
    </template>
  </Dropdown>
</template>
