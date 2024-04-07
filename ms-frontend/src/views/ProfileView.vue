<template>
  <div>
    <header class="sticky top-0 z-40">
      <Navbar :actions="topNavActions" iconPos="right" />
    </header>
    <main class="flex h-[896px] shrink-0 flex-col items-start self-stretch">
      <!--Page title and back button-->
      <div class="flex items-center gap-4 self-stretch p-4">
        <div class="flex flex-[1_0_0] items-center gap-4">
          <!--Back button-->
          <Button text rounded class="h-6 w-6" @click="$router.go(-1)">
            <template #icon>
              <BaseIcon icon="back" />
            </template>
          </Button>

          <!--Name of the page-->
          <div
            class="font-inter text-2xl font-extralight not-italic leading-[normal] text-medium-emphasis"
          >
            Profile
          </div>
        </div>
        <Button text rounded class="flex items-center justify-center gap-3 rounded-lg p-1.5">
          <template #icon>
            <BaseIcon icon="three-dots" />
          </template>
        </Button>
      </div>

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
              :src="user?.image ? createObjectURL(user.image) : profilePicUrl"
              alt="Profile Picture"
              class="bg-lightgray z-10 h-32 w-32 shrink-0 rounded-[128px] bg-cover bg-center bg-no-repeat"
            />

            <!-- <img :src="profilePicUrl" alt="Profile Picture"
                            class="w-32 h-32 shrink-0 rounded-[128px] bg-cover bg-no-repeat bg-center bg-lightgray z-10" /> -->
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
              <div class="flex items-center justify-center gap-2 px-4 py-1">
                <Button
                  rounded
                  :label="followButtonText"
                  iconPos="left"
                  @click="toggleFollowOrUnfollow"
                >
                  <template #icon>
                    <BaseIcon icon="user-plus" />
                  </template>
                </Button>
              </div>

              <!--Share button-->
              <div class="flex items-center justify-center gap-3 px-4 py-1">
                <Button outlined rounded label="Share" iconPos="left">
                  <template #icon>
                    <BaseIcon icon="share" />
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
                <BaseIcon icon="mini-down" class="h-5 w-5" />
                <div class="flex h-6 items-center justify-center gap-2.5">
                  <div
                    class="font-inter text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                  >
                    Sort By
                  </div>
                  <div
                    class="font-inter text-base font-normal not-italic leading-[normal] text-[color:var(--primary-color,#B1BF41)]"
                  >
                    Rating
                  </div>
                </div>
              </div>
              <!--Direction-->
              <div class="flex items-center justify-center gap-3 rounded-lg px-0 py-1">
                <BaseIcon icon="arrow-up" class="h-5 w-5" />
                <div
                  class="font-inter flex h-6 items-center justify-center gap-2.5 text-base font-light not-italic leading-[normal] text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))]"
                >
                  Lowest First
                </div>
              </div>
            </div>
            <div class="h-px self-stretch bg-medium-emphasis opacity-30"></div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import Button from 'primevue/button'
import BaseIcon, { type IconType } from '@/icons/BaseIcon.vue'
import { useRouter } from 'vue-router'
import { userService } from '@/services/userService'
import { User } from '@/types/User'
import { reviewService } from '@/services/reviewService'

const router = useRouter()

const authStore = useAuthStore()
const signedInUser = authStore.user

const userId = ref<string>('')
const user = ref<User>()

const profilePicUrl = ref<string>(
  'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
)

const isFollowed = ref<boolean>()

const reviewCount = ref<number>(0)

const followers = ref<User[]>([])

const createObjectURL = (file: File) => {
  return window.URL.createObjectURL(file)
}

const followButtonText = computed(() => {
  return isFollowed.value ? 'Unfollow' : 'Follow'
})

// Function to toggle follow status
const toggleFollowOrUnfollow = async () => {
  // If not followed yet, follow
  if (isFollowed.value == false) {
    try {
      if (userId.value) {
        await userService.followUser(userId.value)
      }
    } catch (error) {
      console.error('Error following user:', error)
    }
  }
  //If already following, unfollow
  else {
    try {
      if (userId.value) {
        await userService.unfollowUser(userId.value)
      }
    } catch (error) {
      console.error('Error unfollowing user:', error)
    }
  }

  isFollowed.value = !isFollowed.value
}

const topNavActions: MenuOption[] = [
  {
    labelKey: 'sign_out',
    icon: 'arrow-left-start-on-rectangle' as IconType,
    before: () => {
      authStore.signOut()
    },
    to: { name: 'sign-in' }
  },
  {
    labelKey: 'my_profile',
    icon: 'profile' as IconType,
    imageUrl: profilePicUrl.value,
    to: `/profile/${signedInUser?.id}`
  }
]

// Fetch user profile data on component mount
onMounted(async () => {
  userId.value = router.currentRoute.value.params.userId as string // Access userId from router
  try {
    user.value = await userService.getUser(userId.value)
    followers.value = await userService.getUserFollowers(userId.value)
    isFollowed.value = followers.value.some((follower) => follower.id === signedInUser?.id)
  } catch (error) {
    console.error('Error fetching user profile:', error)
  }

  if (user?.value?.username) {
    try {
      const reviews = await reviewService.getUserReviews(user?.value?.username)
      reviewCount.value = reviews.length
    } catch (error: any) {
      // Check if the error is a 404 error
      if (error.response && error.response.status === 404) {
        // If it's a 404 error, don't show it in the console and set reviewCount to 0
        reviewCount.value = 0
      } else {
        // If it's any other error, log it to the console
        console.error('Error fetching user reviews:', error)
      }
    }
  }
})

</script>