<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import { computed, onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'
import { loader, MarkerLibraryType } from '@/utils/useGoogleMaps'
import Button from 'primevue/button'
import BaseIcon from '@/icons/BaseIcon.vue'
import PlaceView from '@/components/PlaceView.vue'
import PlaceItem from '@/components/PlaceItem.vue'
import Dropdown from 'primevue/dropdown'
import ToggleButton from 'primevue/togglebutton'
import MiniChevronDown from '@/icons/MiniChevronDownIcon.vue'
import { reviewService } from '@/services/reviewService'
import { useI18n } from 'vue-i18n'

type PlaceResultData = {
  place: google.maps.places.PlaceResult
  average_rating: number
  total_reviews: number
}

const props = defineProps<{
  query?: string
  placeId?: string
}>()

const i18n = useI18n()

let placesService: google.maps.places.PlacesService

const mapDiv = ref(null)
const map = shallowRef<google.maps.Map>()

const mapInitialized = ref<boolean>(false)

// Start position Zurich
const centerPos = ref({ lat: 47.36667, lng: 8.55 })
const lastPos = ref<google.maps.LatLng | undefined>(undefined)
const lastZoom = ref<number | undefined>(undefined)

const markerList = ref<Map<string, google.maps.marker.AdvancedMarkerElement>>(
  new Map<string, google.maps.marker.AdvancedMarkerElement>()
)

let mapBoundsWatcher: google.maps.MapsEventListener
let mapMarkerWatcher: google.maps.MapsEventListener
const mapBoundsInitialized = ref<boolean>(false)
const mapBounds = ref<google.maps.LatLngBounds>()

const positionChanged = ref<boolean>(false)
const fetchingPosition = ref<boolean>(false)
const fetchingPositionSupported = 'navigator' in window && 'geolocation' in navigator

const placeResultList = ref<PlaceResultData[]>([])
const place = ref<google.maps.places.PlaceResult | null>(null)
const placeInfoOpen = ref<boolean>(false)

const showList = ref<boolean>(true)

const listSortOptions = [
  { name: 'dropdown_selection_rating' },
  { name: 'dropdown_selection_rating_gm' },
  { name: 'dropdown_selection_reviews' },
  { name: 'dropdown_selection_reviews_gm' }
]
const listSortOption = ref(listSortOptions[0])
const ascending = ref<boolean>(false)

onMounted(async () => {
  await loader.importLibrary('maps').then(() => {
    if (mapDiv.value) {
      map.value = new google.maps.Map(mapDiv.value as HTMLElement, {
        center: centerPos.value,
        zoom: 15,
        fullscreenControl: false,
        streetViewControl: false,
        zoomControl: false,
        mapTypeControl: false,
        mapId: import.meta.env.VITE_GOOGLE_API_MAP_ID
      })

      mapBoundsWatcher = google.maps.event.addListener(map.value, 'bounds_changed', setMapBounds)
      mapMarkerWatcher = google.maps.event.addListener(map.value, 'click', (event: any) => {
        if ('placeId' in event) {
          event.stop()
          getPlaceDetails(event.placeId)
        }
      })
    }
  })

  await loader.importLibrary('places').then(({ PlacesService }) => {
    if (!map.value) {
      console.error('Map not initialized!')
      return
    }

    placesService = new PlacesService(map.value)
  })
  mapInitialized.value = true
})

onUnmounted(() => {
  google.maps.event.removeListener(mapBoundsWatcher)
  google.maps.event.removeListener(mapMarkerWatcher)
})

const setMapBounds = function () {
  mapBounds.value = map.value?.getBounds()
  if (mapBounds.value) {
    mapBoundsInitialized.value = true
  }
}

const onSearch = function (query: string | undefined, placeId: string | undefined) {
  if (mapInitialized.value && mapBoundsInitialized.value) {
    if (placeId) {
      getPlaceLocation(placeId)
      getPlaceDetails(placeId)
    } else if (query) {
      querySearch(query, false)
      place.value = null
      placeInfoOpen.value = false
    }
  }
}

watch([mapInitialized, mapBoundsInitialized], () => {
  onSearch(props.query, props.placeId)
})

watch([mapBounds, lastPos, lastZoom], () => {
  if (!mapInitialized.value || !mapBoundsInitialized.value || !lastPos.value) {
    positionChanged.value = false
    return
  }

  positionChanged.value =
    !map.value?.getBounds()?.contains(lastPos.value) || map.value?.getZoom() != lastZoom.value
})

const clearMarker = function () {
  markerList.value.forEach((marker) => {
    marker.map = null
    marker.position = null
  })
  markerList.value.clear()
}

const getPlaceLocation = function (placeId: string) {
  let request = {
    placeId: placeId,
    fields: ['place_id', 'name', 'geometry', 'icon'],
    language: i18n.locale.value
  }

  clearMarker()
  placesService.getDetails(request, callback)
}

const getPlaceDetails = function (placeId: string) {
  if (place.value?.place_id === placeId) {
    placeInfoOpen.value = true
    return
  }
  place.value = null

  let request = {
    placeId: placeId,
    fields: [
      'place_id',
      'name',
      'user_ratings_total',
      'price_level',
      'rating',
      'photos',
      'formatted_phone_number',
      'formatted_address',
      'website',
      'type',
      'editorial_summary',
      'geometry'
    ],
    language: i18n.locale.value
  }

  placesService.getDetails(
    request,
    (
      result: google.maps.places.PlaceResult | null,
      status: google.maps.places.PlacesServiceStatus
    ) => {
      if (status == google.maps.places.PlacesServiceStatus.OK && result) {
        place.value = result
        placeInfoOpen.value = true
      }
    }
  )
}

const querySearch = function (query: string, restrictBounds: boolean) {
  const request: google.maps.places.PlaceSearchRequest = {
    bounds: restrictBounds ? mapBounds.value : undefined,
    location: restrictBounds ? undefined : map.value?.getCenter(),
    radius: 1000,
    keyword: query,
    language: i18n.locale.value
  }
  clearMarker()
  placesService.nearbySearch(request, callbackArray)
}

const callbackArray = async function (
  results: google.maps.places.PlaceResult[] | null,
  status: google.maps.places.PlacesServiceStatus
) {
  if (status == google.maps.places.PlacesServiceStatus.OK && results) {
    const bounds = new google.maps.LatLngBounds()
    const placeIds: string[] = results
      .map((result) => result.place_id)
      .filter((item): item is string => item !== undefined)
    const locationReviews = await reviewService.getReviewByPlaceIds(placeIds).catch(() => [])
    placeResultList.value = []
    results.forEach((result) => {
      const index = locationReviews.findIndex((location) => location.locationId == result.place_id)
      if (index == -1) {
        placeResultList.value.push({ place: result, average_rating: 0, total_reviews: 0 })
      } else {
        placeResultList.value.push({
          place: result,
          average_rating: locationReviews[index].averageRating,
          total_reviews: locationReviews[index].reviews.length
        })
      }
      createMarker(result)
      if (result.geometry?.location) bounds.extend(result.geometry?.location)
    })
    map.value?.fitBounds(bounds)
    lastPos.value = bounds.getCenter()
    lastZoom.value = map.value?.getZoom()
  } else if (status == google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
    lastPos.value = map.value?.getCenter()
    lastZoom.value = map.value?.getZoom()
    placeResultList.value = []
  }
}

const callback = async function (
  result: google.maps.places.PlaceResult | null,
  status: google.maps.places.PlacesServiceStatus
) {
  if (status == google.maps.places.PlacesServiceStatus.OK && result) {
    createMarker(result)
    if (result.place_id) {
      const locationReviews = await reviewService
        .getReviewByPlaceIds([result.place_id])
        .catch(() => [])
      const index = locationReviews.findIndex((location) => location.locationId == result.place_id)
      if (index == -1) {
        placeResultList.value = [{ place: result, average_rating: 0, total_reviews: 0 }]
      } else {
        placeResultList.value = [
          {
            place: result,
            average_rating: locationReviews[index].averageRating,
            total_reviews: locationReviews[index].reviews.length
          }
        ]
      }
    }
    if (result.geometry?.location) {
      map.value?.setCenter(result.geometry?.location)
    }
  }
}

const createMarker = function (place: google.maps.places.PlaceResult) {
  if (!place.geometry?.location) {
    console.error(`Place ${place.name} does not define a geometry object.`)
    return
  }
  if (!place.place_id) {
    console.error(`Place ${place.name} does not define a place_id.`)
    return
  }

  const pin = new google.maps.marker.PinElement({
    glyph: place.icon ? new URL(place.icon) : undefined,
    glyphColor: '#ffffff',
    background: '#B1BF41',
    borderColor: '#B1BF41'
  })

  const marker = new MarkerLibraryType.AdvancedMarkerElement({
    map: map.value,
    position: { lat: place.geometry.location.lat(), lng: place.geometry.location.lng() },
    content: pin.element,
    title: place.name
  })
  markerList.value.set(place.place_id, marker)

  if (place.place_id === props.placeId) {
    ;(marker.content as HTMLElement).style.transform = 'scale(125%) translate(0, -12.5%)'
  }

  // Add a click listener for each marker, and set up the info window.
  marker.addListener('click', () => {
    if (place.place_id) {
      getPlaceDetails(place.place_id)
      markerList.value.forEach((m) => {
        ;(m.content as HTMLElement).style.transform =
          marker == m ? 'scale(125%) translate(0, -12.5%)' : 'translate(0, 0)'
      })
    }
  })
}

const onZoom = function (value: number) {
  map.value?.setZoom(map.value.getZoom()! + value)
}

const centerOnPosition = function () {
  if (fetchingPosition.value) return
  fetchingPosition.value = true
  navigator.geolocation.getCurrentPosition((position) => {
    map.value?.setCenter({ lat: position.coords.latitude, lng: position.coords.longitude })
    fetchingPosition.value = false
  })
}

const onClickPlaceItem = function (placeResult: google.maps.places.PlaceResult) {
  const placeId = placeResult.place_id
  if (placeId) {
    getPlaceDetails(placeId)
    markerList.value.forEach((m, key) => {
      ;(m.content as HTMLElement).style.transform =
        key == placeId ? 'scale(125%) translate(0, -12.5%)' : 'translate(0, 0)'
    })
    showList.value = false
  }
}

const placeResultListSorted = computed(() => {
  return [...placeResultList.value].sort((a: PlaceResultData, b: PlaceResultData) => {
    if (listSortOption.value.name === 'dropdown_selection_rating') {
      return sortPlaceResultByRating(a, b, ascending.value)
    } else if (listSortOption.value.name === 'dropdown_selection_rating_gm') {
      return sortPlaceResultByRatingGoogleMaps(a, b, ascending.value)
    } else if (listSortOption.value.name === 'dropdown_selection_reviews') {
      return sortPlaceResultByReviews(a, b, ascending.value)
    } else if (listSortOption.value.name === 'dropdown_selection_reviews_gm') {
      return sortPlaceResultByReviewsGoogleMaps(a, b, ascending.value)
    }
    return 0
  })
})

const sortPlaceResultByRating = function (
  a: PlaceResultData,
  b: PlaceResultData,
  ascending: boolean
): number {
  return ascending ? a.average_rating - b.average_rating : b.average_rating - a.average_rating
}
const sortPlaceResultByRatingGoogleMaps = function (
  a: PlaceResultData,
  b: PlaceResultData,
  ascending: boolean
): number {
  return ascending
    ? (a.place.rating ?? 0) - (b.place.rating ?? 0)
    : (b.place.rating ?? 0) - (a.place.rating ?? 0)
}
const sortPlaceResultByReviews = function (
  a: PlaceResultData,
  b: PlaceResultData,
  ascending: boolean
): number {
  return ascending ? a.total_reviews - b.total_reviews : b.total_reviews - a.total_reviews
}
const sortPlaceResultByReviewsGoogleMaps = function (
  a: PlaceResultData,
  b: PlaceResultData,
  ascending: boolean
): number {
  return ascending
    ? (a.place.user_ratings_total ?? 0) - (b.place.user_ratings_total ?? 0)
    : (b.place.user_ratings_total ?? 0) - (a.place.user_ratings_total ?? 0)
}
</script>

<template>
  <header class="sticky top-0 z-20 border-b">
    <SignedInTopNav @search="onSearch" />
  </header>

  <main>
    <div class="relative flex h-full w-full overflow-hidden">
      <div
        :class="[
          'relative flex h-full flex-col self-stretch max-sm:absolute max-sm:bottom-0 max-sm:left-0 max-sm:right-0 max-sm:top-0 max-sm:w-full',
          placeResultList.length > 1 ? 'w-[22rem]' : 'w-0',
          showList && placeResultList.length > 1 ? '' : 'max-sm:invisible'
        ]"
      >
        <div
          class="flex h-16 min-h-16 items-center justify-around self-stretch overflow-hidden border-b"
        >
          <Dropdown
            :options="listSortOptions"
            v-model="listSortOption"
            optionLabel="name"
            class="border-none !p-0 text-sm"
          >
            <template #value="slotProps">
              <span class="text-sm">{{ $t('dropdown_sort_by') }}</span
              ><span class="text-sm text-primary">{{ $t(slotProps.value.name) }}</span>
            </template>
            <template #option="slotProps">
              <span class="text-sm">{{ $t('dropdown_sort_by') }}</span
              ><span class="text-sm text-primary">{{ $t(slotProps.option.name) }}</span>
            </template>
            <template #dropdownicon>
              <MiniChevronDown class="!h-5 !w-5" />
            </template>
          </Dropdown>

          <ToggleButton
            v-model="ascending"
            class="border-none text-sm"
            :onLabel="$t('ascending')"
            :offLabel="$t('descending')"
          >
            <template #icon="propScope">
              <BaseIcon
                :icon="propScope.value ? 'arrow-up' : 'arrow-down'"
                class="!h-5 !w-5"
                :stroke-width="1.5"
              />
            </template>
          </ToggleButton>
        </div>
        <div class="divide-y self-stretch overflow-y-auto">
          <PlaceItem
            v-for="placeResult in placeResultListSorted"
            :key="`listResult-${placeResult.place['place_id']}`"
            :place="placeResult.place"
            :average_rating="placeResult.average_rating"
            :reviews_total="placeResult.total_reviews"
            @click="onClickPlaceItem(placeResult.place)"
            :class="[
              placeResult.place.place_id == place?.place_id
                ? 'bg-selection-indicator bg-opacity-5'
                : ''
            ]"
          />
        </div>
        <div class="absolute bottom-4 right-4">
          <Button
            :label="$t('view_map')"
            rounded
            outlined
            @click="showList = false"
            class="sm:invisible"
          >
            <template #icon>
              <BaseIcon icon="map" :size="5" />
            </template>
          </Button>
        </div>
      </div>
      <div
        :class="[
          'relative grow self-stretch max-sm:absolute max-sm:bottom-0 max-sm:left-0 max-sm:right-0 max-sm:top-0',
          showList && placeResultList.length > 1 ? 'max-sm:invisible' : ''
        ]"
      >
        <div id="map" ref="mapDiv" class="h-full w-full outline-none"></div>
        <div class="pointer-events-none absolute bottom-0 left-0 right-0 top-0 flex gap-2 p-2">
          <PlaceView
            v-model:open="placeInfoOpen"
            :place="place"
            class="max-lg:grow max-sm:w-full"
          />
          <div
            :class="[
              'flex flex-col gap-2 overflow-hidden lg:grow',
              placeInfoOpen ? 'max-xl:max-w-0' : 'grow'
            ]"
          >
            <div class="flex w-full">
              <!-- Map Filter -->
            </div>
            <div class="flex w-full justify-center">
              <!-- Center -->
              <Button
                class="pointer-events-auto w-fit"
                v-if="!placeId && positionChanged"
                label="Search this area"
                rounded
                outlined
                @click="
                  () => {
                    if (query) {
                      querySearch(query, true)
                    }
                  }
                "
              >
                <template #icon>
                  <BaseIcon icon="magnifying-glass" :size="5" />
                </template>
              </Button>
            </div>
          </div>
          <div
            :class="[
              'flex w-fit flex-col items-end justify-end gap-2 self-stretch justify-self-end sm:pb-4 ',
              placeInfoOpen ? 'max-lg:grow max-md:max-w-0 max-md:overflow-hidden' : '',
              placeResultList.length > 1 ? 'pb-14' : 'pb-4'
            ]"
          >
            <Button
              v-if="fetchingPositionSupported"
              outlined
              rounded
              class="group pointer-events-auto"
              :disabled="fetchingPosition"
            >
              <template #icon>
                <BaseIcon
                  :icon="fetchingPosition ? 'progress-activity' : 'my-location'"
                  :size="5"
                  :class="{
                    'group-hover:fill-primary': !fetchingPosition,
                    'animate-spin': fetchingPosition
                  }"
                  @click="centerOnPosition"
                />
              </template>
            </Button>
            <div class="group flex flex-col">
              <Button
                outlined
                rounded
                class="pointer-events-auto rounded-b-none border-b-0"
                @click="onZoom(1)"
              >
                <template #icon>
                  <BaseIcon icon="plus" :size="5" :strokeWidth="1.5" />
                </template>
              </Button>
              <Button
                outlined
                rounded
                class="pointer-events-auto rounded-t-none group-hover:border-t-primary"
                @click="onZoom(-1)"
              >
                <template #icon>
                  <BaseIcon icon="minus" :size="5" :strokeWidth="1.5" />
                </template>
              </Button>
            </div>
          </div>
          <Button
            :label="$t('view_list')"
            rounded
            outlined
            @click="showList = true"
            :class="[
              'pointer-events-auto !absolute bottom-6 right-2 h-fit sm:invisible',
              placeResultList.length > 1 ? '' : 'invisible'
            ]"
          >
            <template #icon>
              <BaseIcon icon="list-bullet" :size="5" />
            </template>
          </Button>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
#map iframe + div {
  border: none !important;
}
</style>

<style scoped>
main {
  height: calc(100vh - 65px);
}
</style>
