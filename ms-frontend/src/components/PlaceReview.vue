<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import StarRating from '@/components/StarRating.vue'
import { computed, onMounted, ref, watch } from 'vue'
import { TimeConverter } from '@/utils/timeConverter'
import type { User } from '@/types/User'
import { userService } from '@/services/userService'

const props = withDefaults(
  defineProps<{
    header?: 'USER' | 'PLACE'
    userId: string
    username: string
    text: string
    rating: number
    locationId: string
    locationName: string
    locationType: string
    createdAt: Date
    image?: string
  }>(),
  {
    header: 'USER'
  }
)

const createdHumanReadable = computed(() => {
  return TimeConverter.humanReadable(props.createdAt)
})

const baseUrl = import.meta.env.VITE_PICTURE_BASE_URL
const userProfilePicture = ref<string | null>()
onMounted(() => {
  if (props.header === 'USER') {
    getUserProfilePicture()
  }
})

watch(
  () => [props.userId, props.header],
  (value, oldValue) => {
    if (
      (props.header === 'USER' && value[0] !== oldValue[0]) ||
      (oldValue[1] === 'PLACE' && value[1] === 'USER')
    ) {
      getUserProfilePicture()
    }
  }
)

const getUserProfilePicture = function () {
  userService.getUser(props.userId).then((user: User) => {
    userProfilePicture.value = user.image
  })
}
</script>

<template>
  <div class="flex w-full max-w-full flex-col gap-4 px-4 py-4">
    <div class="flex items-center">
      <template v-if="header === 'USER'">
        <router-link :to="{ name: 'profile', params: { userId: userId } }">
          <div class="flex items-center gap-2">
            <div
              v-if="userProfilePicture"
              class="flex h-8 w-8 items-center justify-center overflow-hidden rounded-full"
            >
              <img
                :src="`${baseUrl}/ms-user/${userProfilePicture}`"
                class="h-full w-full object-cover"
                alt="of user"
              />
            </div>
            <div
              v-else
              class="flex h-8 w-8 items-center justify-center overflow-hidden rounded-full border border-medium-emphasis"
            >
              <BaseIcon icon="user" class="!h-4 !w-4 text-medium-emphasis" />
            </div>
            <div class="flex flex-col">
              <span class="text-xl font-light text-secondary"> {{ username }} </span>
            </div>
          </div>
        </router-link>
      </template>
      <template v-else>
        <router-link :to="{ name: 'map', query: { query: locationName, placeId: locationId } }">
          <div class="flex items-center gap-2">
            <div class="flex flex-col">
              <span class="text-lg font-light text-secondary"> {{ locationName }} </span>
              <span class="-mt-1 text-sm font-light text-medium-emphasis">
                {{ locationType }}
              </span>
            </div>
          </div>
        </router-link>
      </template>
    </div>
    <div class="flex items-center gap-4">
      <div class="flex gap-1">
        <StarRating :rating="rating" class="text-primary" />
      </div>
      <span class="text-sm font-light text-medium-emphasis">{{
        $t(createdHumanReadable.key, { value: createdHumanReadable.value })
      }}</span>
    </div>
    <div class="w-full">
      <span class="text-justify font-light text-medium-emphasis">{{ text }}</span>
    </div>
    <div v-if="image" class="w-full">
      <img :src="`${baseUrl}/ms-review/${image}`" class="w-full object-cover" alt="of review place" />
    </div>
  </div>
</template>
