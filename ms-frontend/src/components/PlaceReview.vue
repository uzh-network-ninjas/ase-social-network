<script setup lang="ts">
import BaseIcon from '@/icons/BaseIcon.vue'
import StarRating from '@/components/StarRating.vue'
import { computed, onMounted, ref, watch } from 'vue'
import { TimeConverter } from '@/utils/timeConverter'
import type { User } from '@/types/User'
import { userService } from '@/services/userService'
import { reviewService } from '@/services/reviewService'
import Button from 'primevue/button'

const props = withDefaults(
  defineProps<{
    header?: 'USER' | 'PLACE' | 'BOTH'
    userId: string
    username: string
    reviewId: string
    text: string
    like_count: number
    liked_by_current_user: boolean
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

const likes = ref<number>(0)
const liked_by_me = ref<boolean>()

const createdHumanReadable = computed(() => {
  return TimeConverter.humanReadable(props.createdAt)
})

const userProfilePicture = ref<string | null>()
onMounted(() => {
  if (props.header !== 'PLACE') {
    getUserProfilePicture()
  }
  likes.value = props.like_count
  liked_by_me.value = props.liked_by_current_user
})

watch(
  () => [props.userId, props.header],
  (value, oldValue) => {
    if (
      (props.header !== 'PLACE' && value[0] !== oldValue[0]) ||
      (oldValue[1] === 'PLACE' && value[1] !== 'PLACE')
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

const toggleLikeOrUnlike = async () => {
  if (!liked_by_me.value) {
    try {
      await reviewService.likeReview(props.reviewId)
      liked_by_me.value = true
      likes.value++
    } catch (error) {
      console.error('Error liking review:', error)
    }
  } else {
    try {
      await reviewService.unlikeReview(props.reviewId)
      liked_by_me.value = false
      likes.value--
    } catch (error) {
      console.error('Error unliking review:', error)
    }
  }
}
</script>

<template>
  <div class="flex w-full max-w-full flex-col gap-4 px-4 py-4">
    <div class="flex flex-col justify-center gap-4">
      <template v-if="header !== 'PLACE'">
        <router-link :to="{ name: 'profile', params: { userId: userId } }">
          <div class="flex items-center gap-2">
            <div
              v-if="userProfilePicture"
              class="flex h-8 w-8 items-center justify-center overflow-hidden rounded-full"
            >
              <img :src="userProfilePicture" class="h-full w-full object-cover" alt="of user" />
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
      <div v-if="header == 'BOTH'" class="h-[1px] w-full bg-black bg-opacity-5"></div>
      <template v-if="header !== 'USER'">
        <router-link :to="{ name: 'map', query: { query: locationName, placeId: locationId } }">
          <div class="flex items-center gap-2">
            <div class="flex flex-col">
              <span class="text-lg font-light text-secondary"> {{ locationName }} </span>
              <span class="-mt-1 text-sm font-light capitalize text-medium-emphasis">
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
      <img
        :src="image"
        class="w-full max-w-[400px] object-cover font-light text-medium-emphasis"
        alt="of review place"
      />
    </div>
    <div class="h-[1px] w-full bg-black bg-opacity-5"></div>
    <div class="flex items-center justify-between self-stretch px-2 py-0">
      <div class="flex items-center gap-2">
        <Button text rounded @click="toggleLikeOrUnlike()">
          <template #icon>
            <BaseIcon
              :icon="liked_by_me ? 'like-solid' : 'like'"
              :class="liked_by_me ? 'text-primary' : 'text-medium-emphasis'"
              :size="5"
            />
          </template>
        </Button>
        <div
          class="font-inter text-base font-light not-italic leading-[normal] text-medium-emphasis"
        >
          {{ likes }}
        </div>
      </div>
    </div>
  </div>
</template>
