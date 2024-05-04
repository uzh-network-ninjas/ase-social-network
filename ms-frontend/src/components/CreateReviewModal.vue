<template>
  <!-- Modal -->
  <div
    class="fixed inset-0 bottom-0 left-0 right-0 top-0 z-50 flex items-center justify-center bg-medium-emphasis px-4 py-20"
  >
    <div
      class="my-auto max-h-full w-full max-w-full overflow-y-auto rounded-lg sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl"
    >
      <div class="modal-content">
        <!-- Review page -->
        <div
          class="flex max-h-[614px] shrink-0 flex-col items-center gap-4 overflow-y-auto rounded-lg bg-white p-4"
        >
          <!-- Place description -->
          <div class="flex flex-col items-start self-stretch">
            <!-- Place name -->
            <div
              class="font-inter text-center text-lg font-light not-italic leading-[normal] text-secondary"
            >
              {{ location.name }}
            </div>
            <!-- Place type -->
            <div
              class="font-inter text-center text-sm font-light capitalize not-italic leading-[normal] text-medium-emphasis"
            >
              {{ location.type }}
            </div>
          </div>
          <!-- Divider -->
          <div class="h-px shrink-0 self-stretch bg-medium-emphasis opacity-60"></div>
          <!-- Input -->
          <div class="flex flex-[1_0_0] flex-col items-start gap-8 self-stretch">
            <!-- Stars -->
            <div class="flex items-start self-stretch">
              <!-- Label -->
              <div class="flex h-6 flex-[1_0_0] items-center">
                <div
                  class="font-inter text-base font-light not-italic leading-[normal] text-medium-emphasis"
                >
                  {{ $t('rating') }}
                </div>
              </div>
              <!-- Rating -->
              <div class="relative flex h-6 w-[152px] items-start gap-2">
                <Button
                  v-for="i in 5"
                  :key="`star-button-${i}`"
                  text
                  rounded
                  @click="submitRating(i)"
                >
                  <template #icon>
                    <BaseIcon
                      :icon="rating >= i ? 'star-solid' : 'star'"
                      :class="[
                        'h-6 w-6 shrink-0',
                        rating >= i ? 'text-primary' : 'text-medium-emphasis'
                      ]"
                    />
                  </template>
                </Button>
                <!-- Error message for rating -->
                <div
                  v-if="!ratingValid"
                  class="font-inter absolute bottom-[-20px] text-[10px] font-light not-italic leading-[normal] text-error"
                >
                  {{ $t('rating_missing_error') }}
                </div>
              </div>
            </div>
            <!-- Text area -->
            <div class="flex flex-[1_0_0] flex-col items-start gap-1 self-stretch">
              <Textarea
                v-model="reviewText"
                type="text"
                :placeholder="$t('review_text_placeholder')"
                class="self-stretch text-base font-light not-italic leading-[normal]"
                rows="4"
              />
              <!-- Error message for review text -->
              <div
                v-if="!textValid"
                class="font-inter text-[10px] font-light not-italic leading-[normal] text-error"
              >
                {{ $t('review_text_error') }}
              </div>
            </div>

            <div
              class="font-inter text-base font-light not-italic leading-[normal] text-medium-emphasis"
            >
              {{ $t('images') }}
            </div>
            <div class="relative w-full">
              <FileUpload v-model="reviewPicture"> </FileUpload>
            </div>
          </div>

          <div class="w-full text-right font-light text-error" v-if="uploadFailed">
            {{ $t('create_review_error') }}
          </div>
          <!-- Divider -->
          <div class="h-px shrink-0 self-stretch bg-medium-emphasis opacity-60"></div>
          <!-- Footer -->
          <div class="flex items-start justify-end self-stretch">
            <!-- Cancel button -->
            <div class="flex items-center justify-center px-2 py-1">
              <Button outlined rounded :label="$t('cancel')" @click="$emit('closeModal')"></Button>
            </div>

            <!-- Post button -->
            <div class="flex items-center justify-center px-2 py-1">
              <Button
                rounded
                :label="$t('post')"
                :disabled="!checkInputValidity()"
                @click="createReview"
              ></Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from 'primevue/button'
import BaseIcon from '@/icons/BaseIcon.vue'
import { ref, watch } from 'vue'
import FileUpload from '@/components/FileUpload.vue'
import { reviewService } from '@/services/reviewService'
import Textarea from 'primevue/textarea'
import { Location } from '@/types/Location'
import type { Review } from '@/types/Review'

const rating = ref<number>(0)
const reviewText = ref<string>('')
const ratingValid = ref<boolean>(false)
const textValid = ref<boolean>(false)
const uploadFailed = ref<boolean>(false)

const props = defineProps<{
  location: Location
}>()

const emit = defineEmits(['closeModal', 'uploadSuccess'])

const reviewPicture = ref<File | null>(null)

watch(reviewText, (newValue) => {
  const reviewTextWords = newValue.trim().split(/\s+/).length
  const reviewTextValue = newValue.trim()
  textValid.value = reviewTextWords > 5 && reviewTextWords < 200 && reviewTextValue !== ''
})

watch(rating, () => {
  ratingValid.value = rating.value > 0
})

const submitRating = (selectedRating: number) => {
  rating.value = selectedRating
}

const checkInputValidity = () => {
  const reviewTextWords = reviewText.value.trim().split(/\s+/).length
  const reviewTextValue = reviewText.value.trim()

  if (reviewTextWords > 5 && reviewTextWords < 200 && reviewTextValue !== '') {
    textValid.value = true
  }
  if (rating.value > 0) ratingValid.value = true
  return ratingValid.value && textValid.value
}

// const testReviews = async () => {
//     const myreviews = ref<Review[]>([])
//   try{
//     myreviews.value = await reviewService.getUserReviews(myId)
//     console.log(myreviews.value.reviews[0])
//   }
//   catch(error){
//     console.log('Error testing myreviews:', error)
//   }
// }

const createReview = async () => {
  if (checkInputValidity()) {
    try {
      uploadFailed.value = false
      // Call createReview method from reviewService
      await reviewService
        .createReview(reviewText.value, rating.value, props.location)
        .then((response: Review) => {
          updateReviewImage(response.id)
        })
      emit('uploadSuccess')
    } catch (error) {
      uploadFailed.value = true
      console.error('Error creating review:', error)
    }
  }
}

const updateReviewImage = async (reviewId: string) => {
  if (reviewPicture.value === null) return
  try {
    await reviewService.appendReviewImage(reviewId, reviewPicture.value)
  } catch (error) {
    console.error('Error updating review image:', error)
  }
}
</script>
