<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import { onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'
import { loader, MarkerLibraryType } from '@/utils/useGoogleMaps'
import Button from 'primevue/button'
import BaseIcon from '@/icons/BaseIcon.vue'

const props = defineProps<{
  query?: string
  placeId?: string
}>()

let placesService: google.maps.places.PlacesService

const mapDiv = ref(null)
const map = shallowRef<google.maps.Map>()

const mapInitialized = ref<boolean>(false)

// Start position Zurich
const centerPos = ref({ lat: 47.36667, lng: 8.55 })
const lastPos = ref<google.maps.LatLng | undefined>(undefined)
const lastZoom = ref<number | undefined>(undefined)

const markerList = ref<google.maps.marker.AdvancedMarkerElement[]>([])

let mapBoundsWatcher: google.maps.MapsEventListener
const mapBoundsInitialized = ref<boolean>(false)
const mapBounds = ref<google.maps.LatLngBounds>()

const positionChanged = ref<boolean>(false)
const fetchingPosition = ref<boolean>(false)
const fetchingPositionSupported = 'navigator' in window && 'geolocation' in navigator

onMounted(async () => {
  await loader.importLibrary('maps').then(({ Map }) => {
    if (mapDiv.value) {
      map.value = new Map(mapDiv.value as HTMLElement, {
        center: centerPos.value,
        zoom: 15,
        fullscreenControl: false,
        streetViewControl: false,
        zoomControl: false,
        mapTypeControl: false,
        mapId: import.meta.env.VITE_GOOGLE_API_MAP_ID
      })

      mapBoundsWatcher = google.maps.event.addListener(map.value, 'bounds_changed', setMapBounds)
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
})

const setMapBounds = function () {
  mapBounds.value = map.value?.getBounds()
  if (mapBounds.value) {
    mapBoundsInitialized.value = true
  }
}

const onSearchUpdated = function (query: string, placeId: string | undefined) {
  if (mapInitialized.value && mapBoundsInitialized.value) {
    if (placeId) {
      getPlaceLocation(placeId)
    } else if (query) {
      querySearch(query, false)
    }
  }
}

watch([mapInitialized, mapBoundsInitialized], () => {
  if (mapInitialized.value && mapBoundsInitialized.value) {
    if (props.placeId) {
      getPlaceLocation(props.placeId)
    } else if (props.query) {
      querySearch(props.query, false)
    }
  }
})

watch([mapBounds, lastPos, lastZoom], () => {
  if (!mapInitialized.value || !mapBoundsInitialized.value || !lastPos.value) {
    positionChanged.value = false
    return
  }

  positionChanged.value =
    !map.value?.getBounds()?.contains(lastPos.value!) || map.value?.getZoom() != lastZoom.value
})

const clearMarker = function () {
  markerList.value.forEach((marker) => {
    marker.map = null
    marker.position = null
  })
  markerList.value = []
}

const getPlaceLocation = function (placeId: string) {
  let request = {
    placeId: placeId,
    fields: ['name', 'geometry', 'icon']
  }

  clearMarker()
  placesService.getDetails(request, callback)
}

const querySearch = function (query: string, restrictBounds: boolean) {
  const request: google.maps.places.PlaceSearchRequest = {
    bounds: restrictBounds ? mapBounds.value : undefined,
    location: restrictBounds ? undefined : map.value?.getCenter(),
    radius: 1000,
    keyword: query
  }
  clearMarker()
  placesService.nearbySearch(request, callbackArray)
}

const callbackArray = function (
  results: google.maps.places.PlaceResult[] | null,
  status: google.maps.places.PlacesServiceStatus
) {
  if (status == google.maps.places.PlacesServiceStatus.OK && results) {
    const bounds = new google.maps.LatLngBounds()
    results.forEach((result) => {
      createMarker(result)
      if (result.geometry?.location) bounds.extend(result.geometry?.location)
    })
    map.value?.fitBounds(bounds)
    lastPos.value = bounds.getCenter()
    lastZoom.value = map.value?.getZoom()
  } else if (google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
    lastPos.value = map.value?.getCenter()
    lastZoom.value = map.value?.getZoom()
  }
}

const callback = function (
  result: google.maps.places.PlaceResult | null,
  status: google.maps.places.PlacesServiceStatus
) {
  if (status == google.maps.places.PlacesServiceStatus.OK && result) {
    createMarker(result)
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
  markerList.value.push(marker)
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
</script>

<template>
  <header class="sticky top-0 z-20 border-b">
    <SignedInTopNav @search="onSearchUpdated" />
  </header>

  <main>
    <div class="relative flex h-full w-full flex-row overflow-hidden">
      <div class="flex w-64 flex-col self-stretch">
        <div class="h-16 self-stretch border-b">
          <!-- List Header -->
        </div>
        <div class="self-stretch">
          <!-- List View -->
        </div>
      </div>
      <div class="relative grow self-stretch">
        <div ref="mapDiv" class="h-full w-full outline-none"></div>
        <div class="pointer-events-none absolute bottom-0 left-0 right-0 top-0 flex p-2">
          <div class="flex grow flex-col gap-2">
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
          <div class="flex w-fit flex-col justify-end gap-2 self-stretch">
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
            <div class="group flex flex-col pb-4">
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
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  height: calc(100vh - 65px);
}
</style>
