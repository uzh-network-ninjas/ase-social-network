<script setup lang="ts">
import SignedInTopNav from '@/components/SignedInTopNav.vue'
import SideMenu, { type SideMenuOption } from '@/components/SideMenu.vue'
import PlaceReview from '@/components/PlaceReview.vue'
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { Review } from '@/types/Review'
import { reviewService } from '@/services/reviewService'

const sideNavActions: SideMenuOption[] = [
  {
    labelKey: 'map',
    icon: 'map',
    to: { name: 'map' }
  },
  {
    labelKey: 'search_user',
    icon: 'user-plus',
    to: { name: 'search-user' }
  }
]

const sideMenuContainer = ref<HTMLElement>()
const sideBarHeight = ref<number>(0)
const reviews = ref<Review[]>([])
const intersectionObserver = ref<IntersectionObserver>()
const fetching = ref<boolean>(false)

onMounted(() => {
  sideBarHeight.value = sideMenuContainer.value?.clientHeight ?? 0
  window.addEventListener('scroll', onScroll)
  intersectionObserver.value = new IntersectionObserver(onIntersect)
  getReviews()
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

const onIntersect = function (
  entries: IntersectionObserverEntry[],
  observer: IntersectionObserver
) {
  const element = entries[0]
  if (element.isIntersecting && !fetching.value) {
    getReviews(reviews.value[reviews.value.length - 1].createdAt)
    observer.disconnect()
  }
}

const getReviews = function (timestamp_cursor?: Date) {
  fetching.value = true
  reviewService
    .getReviews(timestamp_cursor)
    .then((nextReviews: Review[]) => {
      reviews.value.push(...nextReviews)
      nextTick(() => {
        const element = document.getElementById('observed-element')
        if (element) {
          intersectionObserver.value?.observe(element)
        }
      })
    })
    .catch((error) => {
      if (error.response.status == 404) {
        intersectionObserver.value?.disconnect()
      } else {
        console.error(error)
      }
    })
    .finally(() => {
      fetching.value = false
    })
}

const previousPageOffset = ref<number>(0)
const scrollingDown = ref<boolean>(false)
const onScroll = function () {
  const currentPageOffset = window.scrollY
  scrollingDown.value = previousPageOffset.value < currentPageOffset
  previousPageOffset.value = currentPageOffset
}
</script>

<template>
  <header class="sticky top-0 z-40">
    <SignedInTopNav />
    <div
      class="z-40 bg-white py-3 max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-2 sm:bg-transparent sm:px-4"
    >
      <h1 class="ml-8 text-2xl font-extralight text-medium-emphasis">{{ $t('home') }}</h1>
    </div>
  </header>
  <main class="sm:mx-8">
    <div class="relative flex w-full flex-col gap-8 sm:flex-row">
      <div
        ref="sideMenuContainer"
        :style="`--side-bar-top: ${120 - (scrollingDown ? sideBarHeight : 0)}px;`"
        :class="
          '' +
          'top-transition bg-background ' +
          'sticky top-[7.5rem] z-10 ' +
          'max-sm:w-full max-sm:border-b max-sm:border-b-medium-emphasis max-sm:px-4 max-sm:py-4 max-sm:transition-[top] max-sm:duration-500 ' +
          'sm:top-[8.5rem] sm:my-4 sm:h-auto sm:self-start'
        "
      >
        <SideMenu :actions="sideNavActions" />
      </div>
      <div class="flex grow flex-col pb-4 max-sm:w-full max-sm:divide-y max-sm:px-4">
        <PlaceReview
          v-for="(review, index) in reviews"
          :id="index == reviews.length - 5 ? 'observed-element' : ''"
          :key="review.id"
          header="BOTH"
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
          <span class="font-light text-medium-emphasis">{{ $t('no_reviews_in_feed') }}</span>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
@media (max-width: 640px) {
  .top-transition {
    top: var(--side-bar-top, 0px);
  }
}
</style>
