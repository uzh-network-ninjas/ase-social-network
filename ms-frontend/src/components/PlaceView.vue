<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseIcon from '@/icons/BaseIcon.vue'
import Button from 'primevue/button'
import PlaceReview from '@/components/PlaceReview.vue'
import CreateReviewModal from '@/components/CreateReviewModal.vue'
import StarRating from '@/components/StarRating.vue'
import { Review } from '@/types/Review'
import { reviewService } from '@/services/reviewService'
import { LocationReviews } from '@/types/LocationReviews'
import { Location } from '@/types/Location'

const props = defineProps<{
  place: google.maps.places.PlaceResult | null
  open: boolean
}>()

defineEmits<(e: 'update:open', value: boolean) => void>()

const container = ref<HTMLElement>()
const reviews = ref<Review[]>([])
const average_rating = ref<number>(0.0)
const showCreateModal = ref<boolean>(false)
const location = ref<Location | null>()
const uploadSuccess = ref<boolean>(false)

watch(
  () => [props.place],
  () => {
    container.value?.scrollTo(0, 0)
    uploadSuccess.value = false
    getReviews()
    updateLocation()
  }
)

const onCreateSuccess = function () {
  closeCreateModal()
  uploadSuccess.value = true
}

const updateLocation = function () {
  if (props.place?.['place_id']) {
    location.value = new Location({
      id: props.place['place_id'],
      name: props.place['name'] ?? 'NO NAME',
      type: props.place['types']?.[0]?.replace(/_/g, ' ') ?? '',
      coordinates: {
        x: props.place['geometry']?.location?.lat().toString() ?? '0',
        y: props.place['geometry']?.location?.lng().toString() ?? '0'
      }
    })
  } else {
    location.value = undefined
  }
}

const openCreateModal = function () {
  showCreateModal.value = true
  uploadSuccess.value = false
  console.log('peep')
}

const closeCreateModal = function () {
  showCreateModal.value = false
}

const copyTextToClipboard = function (text: string) {
  navigator.clipboard.writeText(text)
}

const openInNewTab = function (url: string) {
  window.open(url)
}

const getReviews = function () {
  const placeId = props.place?.['place_id']
  if (placeId) {
    reviewService
      .getReviewByPlaceIds([placeId])
      .then((locationReviews: LocationReviews[]) => {
        if (locationReviews.length != 1 || locationReviews[0].locationId !== placeId) {
          reviews.value = []
          average_rating.value = 0.0
        } else {
          reviews.value = locationReviews[0].reviews
          average_rating.value = locationReviews[0].averageRating
        }
      })
      .catch((error) => {
        if (error.response?.status === 404) {
          reviews.value = []
          average_rating.value = 0.0
        }
      })
  }
}
</script>

<template>
  <div
    :class="[
      'pointer-events-auto relative flex h-full flex-col rounded-lg bg-background',
      open ? 'max-w-[27rem]' : 'max-w-[0]'
    ]"
  >
    <div
      ref="container"
      class="relative flex h-full w-full flex-col divide-y overflow-auto rounded-lg"
    >
      <div class="max-h-60 min-h-60 w-full">
        <img
          v-if="place?.photos && place.photos.length > 0"
          :src="place['photos'][0].getUrl({ maxWidth: 432 })"
          class="h-full w-full object-cover"
          aria-hidden="true"
          alt=""
        />
      </div>
      <div class="flex flex-col gap-4 px-4 py-4">
        <div class="flex flex-col">
          <h1 class="text-2xl text-secondary">{{ place?.name }}</h1>
          <div class="flex items-center gap-2 text-sm font-light text-medium-emphasis">
            <span class="capitalize">{{ place?.types?.[0]?.replace(/_/g, ' ') }}</span>
            <span v-if="place?.types?.[0] && place?.price_level">·</span>
            <span><template v-for="i in place?.price_level" :key="i">$</template></span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-medium-emphasis">{{
            (average_rating ?? 0.0).toLocaleString(undefined, {
              minimumFractionDigits: 1,
              maximumFractionDigits: 1
            })
          }}</span>
          <StarRating :rating="average_rating" class="text-primary" />
          <span class="text-xs text-medium-emphasis"
            >{{ `(${reviews.length ?? 0})` }} · {{ $t('your_follows') }}</span
          >
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-medium-emphasis">{{
            (place?.['rating'] ?? 0.0).toLocaleString(undefined, {
              minimumFractionDigits: 1,
              maximumFractionDigits: 1
            })
          }}</span>
          <StarRating :rating="place?.['rating']" class="text-google-maps-star" />
          <span class="text-xs text-medium-emphasis"
            >{{ `(${place?.['user_ratings_total'] ?? 0})` }} · Google Maps</span
          >
        </div>
      </div>
      <div
        v-if="place?.formatted_address || place?.website || place?.formatted_phone_number"
        class="flex flex-col px-2 py-4"
      >
        <div
          v-if="place?.['formatted_address']"
          class="group flex items-center gap-4 rounded-lg px-2 py-1 hover:bg-selection-indicator hover:bg-opacity-5"
        >
          <BaseIcon class="text-secondary" icon="map-pin" :strokeWidth="1.5" />
          <span class="grow text-sm font-light text-medium-emphasis">{{
            place?.['formatted_address']
          }}</span>
          <div class="flex gap-1">
            <Button
              rounded
              class="invisible border-none bg-transparent hover:bg-white group-hover:visible"
              @click="copyTextToClipboard(place?.['formatted_address'])"
              aria-label="copy address URL to clipboard"
            >
              <template #icon>
                <BaseIcon
                  class="text-medium-emphasis"
                  icon="clipboard-document"
                  :size="5"
                  :strokeWidth="1.5"
                />
              </template>
            </Button>
          </div>
        </div>
        <div
          v-if="place?.website"
          class="group flex items-center gap-4 rounded-lg px-2 py-1 hover:bg-selection-indicator hover:bg-opacity-5"
        >
          <BaseIcon class="text-secondary" icon="globe-alt" :strokeWidth="1.5" />
          <span class="grow text-sm font-light text-medium-emphasis">{{ place?.['website'] }}</span>
          <div class="flex gap-1">
            <Button
              rounded
              class="invisible border-none bg-transparent hover:bg-white group-hover:visible"
              @click="copyTextToClipboard(place?.['website'])"
              aria-label="copy website URL to clipboard"
            >
              <template #icon>
                <BaseIcon
                  class="text-medium-emphasis"
                  icon="clipboard-document"
                  :size="5"
                  :strokeWidth="1.5"
                />
              </template>
            </Button>
            <Button
              rounded
              class="invisible border-none bg-transparent hover:bg-white group-hover:visible"
              @click="openInNewTab(place?.['website'])"
              aria-label="open website in new tab"
            >
              <template #icon>
                <BaseIcon
                  class="text-medium-emphasis"
                  icon="arrow-top-right-on-square"
                  :size="5"
                  :strokeWidth="1.5"
                />
              </template>
            </Button>
          </div>
        </div>
        <div
          v-if="place?.formatted_phone_number"
          class="group flex items-center gap-4 rounded-lg px-2 py-1 hover:bg-selection-indicator hover:bg-opacity-5"
        >
          <BaseIcon class="text-secondary" icon="phone" :strokeWidth="1.5" />
          <span class="grow text-sm font-light text-medium-emphasis">{{
            place?.['formatted_phone_number']
          }}</span>
          <div class="flex gap-1">
            <Button
              rounded
              class="invisible border-none bg-transparent hover:bg-white group-hover:visible"
              @click="copyTextToClipboard(place?.['formatted_phone_number'])"
              aria-label="copy phone number URL to clipboard"
            >
              <template #icon>
                <BaseIcon
                  class="text-medium-emphasis"
                  icon="clipboard-document"
                  :size="5"
                  :strokeWidth="1.5"
                />
              </template>
            </Button>
          </div>
        </div>
      </div>
      <div class="flex flex-col items-center gap-4 px-2 py-4">
        <h2 class="text-xl uppercase tracking-[6px] text-medium-emphasis">Reviews</h2>
        <Button class="w-full" rounded :label="$t('create_review')" @click="openCreateModal()" />
        <div class="w-full text-center font-light text-secondary" v-if="uploadSuccess">
          {{ $t('create_review_success') }}
        </div>
        <CreateReviewModal
          v-if="showCreateModal && location"
          v-model:location="location"
          @closeModal="closeCreateModal"
          @uploadSuccess="onCreateSuccess"
        />
      </div>
      <div class="flex flex-col items-center divide-y">
        <PlaceReview
          v-for="review in reviews"
          :key="review.id"
          :userId="review.userId"
          :username="review.username"
          :review-id="review.id"
          :text="review.text"
          :like_count="review.like_count"
          :liked_by_current_user="review.liked_by_current_user"
          :rating="review.rating"
          :locationId="review.location.id"
          :locationName="review.location.name"
          :locationType="review.location.type"
          :createdAt="review.createdAt"
          :image="review.image"
        />
        <div v-if="reviews.length === 0" class="w-full px-2 py-4 text-center">
          <span class="font-light text-medium-emphasis">{{ $t('no_reviews_for_place') }}</span>
        </div>
      </div>
    </div>
    <div
      v-if="place || open"
      :class="[
        'absolute right-0 top-1/2 -translate-y-1/2 translate-x-full cursor-pointer rounded-r-lg bg-background py-4',
        open ? 'rounded-l-none' : 'rounded-l-md'
      ]"
      @click="$emit('update:open', !open)"
    >
      <BaseIcon
        :class="['h-5 w-5 text-medium-emphasis', open ? 'rotate-0' : 'rotate-180']"
        :icon="'mini-chevron-left'"
        :stroke-width="1.5"
      />
    </div>
  </div>
</template>
