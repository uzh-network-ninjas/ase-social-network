<script setup lang="ts">
import StarRating from '@/components/StarRating.vue'

defineProps<{
  place: google.maps.places.PlaceResult | null
  average_rating: number
  reviews_total: number
}>()
</script>

<template>
  <div class="gap flex cursor-pointer gap-4 py-2 hover:bg-selection-indicator hover:bg-opacity-5">
    <div class="flex grow flex-col gap-1 overflow-hidden">
      <div class="flex flex-col self-stretch px-2">
        <h1 class="truncate text-base font-light text-secondary">{{ place?.name }}</h1>
      </div>
      <div class="flex flex-col gap-0 px-2">
        <div class="flex items-center gap-2">
          <span class="text-xs font-light text-medium-emphasis">{{
            (average_rating ?? 0.0).toLocaleString(undefined, {
              minimumFractionDigits: 1,
              maximumFractionDigits: 1
            })
          }}</span>
          <StarRating :rating="average_rating" size="small" class="text-primary" />
          <span class="text-xs font-light text-medium-emphasis"
            >{{ `(${reviews_total ?? 0})` }}
          </span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-light text-medium-emphasis">{{
            (place?.['rating'] ?? 0.0).toLocaleString(undefined, {
              minimumFractionDigits: 1,
              maximumFractionDigits: 1
            })
          }}</span>
          <StarRating :rating="place?.['rating']" size="small" class="text-google-maps-star" />
          <span class="text-xs font-light text-medium-emphasis"
            >{{ `(${place?.['user_ratings_total'] ?? 0})` }}
          </span>
        </div>
      </div>
      <div class="flex flex-col gap-1">
        <div class="flex items-center gap-1 px-2 text-xs font-light text-medium-emphasis">
          <span class="capitalize">{{ place?.types?.[0]?.replace(/_/g, ' ') }}</span>
          <span v-if="place?.types?.[0] && place?.price_level">·</span>
          <span><template v-for="i in place?.price_level" :key="i">$</template></span>
        </div>
        <div class="flex self-stretch px-2">
          <span class="text-xs font-light text-medium-emphasis">{{ place?.['vicinity'] }}</span>
        </div>
      </div>
    </div>
    <div class="flex items-center justify-center self-stretch pr-4">
      <div class="h-20 w-20">
        <img
          v-if="place?.photos && place.photos.length > 0"
          :src="place['photos'][0].getUrl({ maxWidth: 160 })"
          class="h-full w-full rounded-lg object-cover"
          aria-hidden="true"
          alt=""
        />
      </div>
    </div>
  </div>
</template>
