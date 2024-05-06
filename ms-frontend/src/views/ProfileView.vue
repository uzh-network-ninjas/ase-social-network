<template>
  <div>
    <header class="sticky top-0 z-40">
      <SignedInTopNav />
      <PageHeader :label="$t('profile')" />
    </header>
    <main class="flex h-[896px] shrink-0 flex-col items-start self-stretch">
      <!--Page-->
      <div class="flex flex-[1_0_0] flex-col items-center gap-8 self-stretch px-0 py-8">
        <!--Profile information-->
        <div class="flex items-start justify-center gap-8 self-stretch px-8 py-0">
          <!-- Profile picture with masked green rectangle -->
          <div
            class="relative flex h-[136px] w-[136px] items-center justify-center rounded-[128px]"
          >
            <!-- Green rectangle with rotation -->
            <div
              class="absolute h-[177.361px] w-[67.951px] rotate-[-47.552deg] overflow-hidden bg-primary"
              style="clip-path: circle(50.5%)"
            ></div>
            <div
              class="absolute left-0.5 top-0.5 h-[132px] w-[132px] rounded-[128px] bg-white"
            ></div>
            <!-- Profile picture -->
            <img
              :src="profilePicUrl"
              alt="of user"
              class="bg-lightgray z-10 h-32 w-32 shrink-0 rounded-[128px] bg-cover bg-center bg-no-repeat object-cover"
            />
          </div>

          <!--Information-->
          <div class="flex flex-[1_0_0] flex-col items-start gap-4">
            <!--Username-->
            <div
              class="text-center text-2xl font-light not-italic leading-[normal] text-[color:var(--secondary-color,#5C917F)]"
            >
              {{ user?.username }}
            </div>

            <!--Stats-->
            <div class="flex items-center justify-center gap-8">
              <!--Review count-->
              <div class="flex flex-col items-start justify-center">
                <div
                  class="self-stretch text-center text-2xl font-light not-italic leading-[normal] text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))]"
                >
                  {{ reviewCount }}
                </div>
                <div
                  class="self-stretch text-center text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                >
                  Reviews
                </div>
              </div>

              <!--Divider-->
              <div class="w-px self-stretch bg-medium-emphasis opacity-30"></div>

              <!--Follower count-->
              <div class="flex flex-col items-start justify-center">
                <div
                  class="self-stretch text-center text-2xl font-light not-italic leading-[normal] text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))]"
                >
                  {{ user?.followers.length }}
                </div>
                <div
                  class="self-stretch text-center text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                >
                  Followers
                </div>
              </div>

              <!--Divider-->
              <div class="w-px self-stretch bg-medium-emphasis opacity-30"></div>

              <!--Follows count-->
              <div class="flex flex-col items-start justify-center">
                <div
                  class="self-stretch text-center text-2xl font-light not-italic leading-[normal] text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))]"
                >
                  {{ user?.following.length }}
                </div>
                <div
                  class="self-stretch text-center text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                >
                  Follows
                </div>
              </div>
            </div>

            <!--Actions-->
            <div class="flex items-start justify-center gap-8">
              <!--Follow button-->
              <div
                v-if="userId !== authStore.user?.id"
                class="flex items-center justify-center gap-2 px-4 py-1"
              >
                <Button
                  rounded
                  :label="followButtonText"
                  iconPos="left"
                  @click="toggleFollowOrUnfollow"
                >
                  <template #icon>
                    <BaseIcon icon="user-plus" :size="5" />
                  </template>
                </Button>
              </div>

              <div v-else class="flex items-center justify-center gap-2 px-4 py-1">
                <router-link :to="{ name: 'settings-profile' }" custom v-slot="{ navigate }">
                  <Button rounded :label="$t('edit')" iconPos="left" @click="navigate">
                    <template #icon>
                      <BaseIcon icon="pencil-square" :size="5" />
                    </template>
                  </Button>
                </router-link>
              </div>

              <!--Share button-->
              <div class="flex items-center justify-center gap-3 px-4 py-1">
                <Button outlined rounded :label="$t('share')" iconPos="left">
                  <template #icon>
                    <BaseIcon icon="share" :size="5" :strokeWidth="1.5" />
                  </template>
                </Button>
              </div>
            </div>
          </div>
        </div>

        <!--Reviews-->
        <div class="flex flex-col items-center self-stretch">
          <!--Page title-->
          <div class="flex flex-col items-start gap-4 self-stretch">
            <!--Divider-->
            <div class="h-px self-stretch bg-medium-emphasis opacity-30"></div>
            <!--Title-->
            <div
              class="font-inter flex flex-[1_0_0] items-start gap-2.5 self-stretch px-8 py-0 text-2xl font-normal uppercase not-italic leading-[normal] tracking-[6px] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
            >
              Reviews
            </div>
            <!--Sorting-->
            <div class="flex items-start gap-8 self-stretch px-8 py-0">
              <!--Sort by-->
              <div class="flex items-center justify-center gap-3 rounded-lg px-0 py-1">
                <!--Front Icon-->
                <BaseIcon icon="mini-down" />
                <div class="flex h-6 items-center justify-center gap-2.5">
                  <div
                    class="font-inter text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                  >
                    {{ $t('dropdown_sort_by') }}
                  </div>
                  <div
                    class="font-inter text-base font-normal not-italic leading-[normal] text-[color:var(--primary-color,#B1BF41)]"
                  >
                    {{ $t('dropdown_selection_rating') }}
                  </div>
                </div>
              </div>
              <!--Direction-->
              <div class="flex items-center justify-center gap-3 rounded-lg px-0 py-1">
                <BaseIcon icon="arrow-up" :size="5" />
                <div
                  class="font-inter flex h-6 items-center justify-center gap-2.5 text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                >
                  {{ $t('ascending') }}
                </div>
              </div>
            </div>
            <div class="h-px self-stretch">
              <div class="flex flex-col divide-y px-8">
                <PlaceReview
                  v-for="review in reviews"
                  :header="'PLACE'"
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
                  <span class="font-light text-medium-emphasis">{{
                    $t('no_reviews_for_user')
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Button from 'primevue/button'
import BaseIcon from '@/icons/BaseIcon.vue'
import { userService } from '@/services/userService'
import { User } from '@/types/User'
import { Review } from '@/types/Review'
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import PageHeader from '@/components/PageHeader.vue'
import PlaceReview from '@/components/PlaceReview.vue'
import { reviewService } from '@/services/reviewService'

const props = defineProps<{
  userId: string
}>()

const authStore = useAuthStore()

const user = ref<User>()

const profilePicUrl = computed<string>(() => {
  if (user.value?.image) {
    return user.value.image
  } else {
    return 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
  }
})

const isFollowed = ref<boolean>()
const reviewCount = ref<number>(0)
const reviews = ref<Review[]>([])

// // Review data
// const placeName = ref<string>('Placeholder Name')
// const placeType = ref<string>('Placeholder Type')
// const placeRating = ref<number>(3)

// Fetch user profile data on component mount
onMounted(() => {
  getUserData()
  getReviews()
})
// Fetch user profile data on userId change
watch(
  () => props.userId,
  () => {
    getUserData()
    getReviews()
  }
)

const getUserData = async () => {
  try {
    user.value = await userService.getUser(props.userId)
    isFollowed.value = user.value?.followers.some((follower) => {
      return follower === authStore.user?.id
    })
  } catch (error) {
    console.error('Error fetching user profile:', error)
  }
}

const followButtonText = computed(() => {
  return isFollowed.value ? 'Unfollow' : 'Follow'
})

const getReviews = async () => {
  try {
    reviews.value = await reviewService.getUserReviews(props.userId)
  } catch (error: any) {
    if (error.response.status == 404) {
      reviews.value = []
    } else console.error('Error fetching user reviews:', error)
  }
}

// Function to toggle follow status
const toggleFollowOrUnfollow = async () => {
  // If not followed yet, follow

  if (!isFollowed.value) {
    try {
      if (props.userId) {
        await userService.followUser(props.userId)
      }
    } catch (error) {
      console.error('Error following user:', error)
    }
  }
  //If already following, unfollow
  else {
    try {
      if (props.userId) {
        await userService.unfollowUser(props.userId)
      }
    } catch (error) {
      console.error('Error unfollowing user:', error)
    }
  }
  await getUserData()
}
</script>
