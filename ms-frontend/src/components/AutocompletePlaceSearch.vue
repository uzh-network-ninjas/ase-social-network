<script setup lang="ts">
import AutoComplete from 'primevue/autocomplete'
import InputIcon from 'primevue/inputicon'
import IconField from 'primevue/iconfield'
import BaseIcon from '@/icons/BaseIcon.vue'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { autocompleteService } from '@/utils/useGoogleMaps'

const router = useRouter()
const route = useRoute()

const emit = defineEmits<(e: 'search', query: string, placeId: string | undefined) => void>()

const autocomplete = ref<string>(route.query.query as string)
const items = ref<google.maps.places.QueryAutocompletePrediction[] | null>(null)

const search = (event: any) => {
  // Bias search to center rof Zurich
  const loc = new google.maps.LatLng(47.36667, 8.55)
  autocompleteService.getQueryPredictions(
    { input: event.query, location: loc, radius: 100 },
    callback
  )
}

const callback = function (
  predictions: google.maps.places.QueryAutocompletePrediction[] | null,
  status: google.maps.places.PlacesServiceStatus
) {
  if (status == google.maps.places.PlacesServiceStatus.OK && predictions) {
    items.value = predictions
  }
}

const clearSearchTerm = function () {
  autocomplete.value = ''
}

const getPreviousUnMarkedSegment = function (
  option: google.maps.places.AutocompletePrediction,
  index: number
) {
  if (index <= 0) {
    return ''
  }
  const offset = option.structured_formatting['main_text_matched_substrings'][index - 1].offset
  const length = option.structured_formatting['main_text_matched_substrings'][index - 1].length
  const startIndex = option.structured_formatting['main_text_matched_substrings'][index].offset

  return option.structured_formatting['main_text'].slice(offset + length, startIndex)
}

const getLastUnmarkedSegment = function (
  option: google.maps.places.AutocompletePrediction,
  lastMatch: google.maps.places.PredictionSubstring
) {
  return option.structured_formatting['main_text'].slice(lastMatch.offset + lastMatch.length + 1)
}

const getCurrentMarkedSegment = function (
  option: google.maps.places.AutocompletePrediction,
  match: google.maps.places.PredictionSubstring
) {
  return option.structured_formatting['main_text'].slice(match.offset, match.length)
}

const getPredictionSubString = function (
  option: google.maps.places.AutocompletePrediction
): google.maps.places.PredictionSubstring[] {
  return option.structured_formatting['main_text_matched_substrings']
}

const onUpdate = function (value: any) {
  if (typeof value == 'object') {
    autocomplete.value = value.description
    router.push({ name: 'map', query: { query: value.description, placeId: value['place_id'] } })
    emit('search', value.description, value['place_id'])
  } else {
    autocomplete.value = value
  }
}

const onEnter = function () {
  emit('search', autocomplete.value, undefined)
}
</script>

<template>
  <IconField class="mx-4 grow" iconPosition="right">
    <AutoComplete
      :modelValue="autocomplete"
      @update:modelValue="onUpdate"
      :suggestions="items ?? []"
      @complete="search"
      variant="filled"
      :pt="{
        root: {
          class: ['relative', 'inline-flex', 'w-full', '!pr-0']
        }
      }"
      :placeholder="$t('search_place')"
      @keyup.enter="onEnter"
    >
      <template #option="{ option }: { option: google.maps.places.AutocompletePrediction }">
        <div class="flex items-center gap-4">
          <BaseIcon
            :icon="option.place_id ? 'map-pin' : 'magnifying-glass'"
            class="!h-5 !w-5"
            :stroke-width="1"
          />
          <div class="flex items-baseline">
            <template
              v-for="(match, index) in getPredictionSubString(option)"
              :key="`${match.offset}-${match.length}`"
            >
              <span v-if="index > 0">{{ getPreviousUnMarkedSegment(option, index) }}</span>
              <span class="font-medium">{{ getCurrentMarkedSegment(option, match) }}</span>
              <span v-if="index == getPredictionSubString(option).length - 1">{{
                getLastUnmarkedSegment(option, match)
              }}</span>
            </template>
            <span :class="{ 'ml-1 text-sm': option.place_id }">
              {{
                (option as google.maps.places.AutocompletePrediction)['structured_formatting'][
                  'secondary_text'
                ]
              }}</span
            >
          </div>
        </div>
      </template>
    </AutoComplete>
    <InputIcon>
      <BaseIcon
        v-if="autocomplete"
        icon="x-mark"
        :size="5"
        :stroke-width="1"
        class="cursor-pointer rounded-full outline-none ring-offset-1 hover:text-primary focus-visible:text-primary focus-visible:ring-1 focus-visible:ring-primary"
        @click="clearSearchTerm"
        @keyup.space="clearSearchTerm"
        tabindex="0"
      />
      <BaseIcon v-else icon="magnifying-glass" :size="5" />
    </InputIcon>
  </IconField>
</template>
