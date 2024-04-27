<template>
    <div>
        <button @click="openModal">Open Modal</button>

        <!-- Modal -->
        <div class="fixed w-full h-full flex items-center justify-center left-0 top-0 bg-medium-emphasis"
            v-if="showModal">
            <div class="fixed p-0 rounded-[5px]">
                <div class="modal-content">
                    <!-- Review page -->
                    <div class="flex w-[508px] h-[614px] flex-col items-center gap-4 shrink-0 p-4 rounded-lg bg-white
                    h-[500px] overflow-y-auto">

                        <!-- Place description -->
                        <div class="flex flex-col items-start self-stretch">
                            <!-- Place name -->
                            <div
                                class="text-secondary text-center text-lg not-italic font-light leading-[normal] font-inter">
                                {{ placeName }}
                            </div>
                            <!-- Place type -->
                            <div
                                class="text-medium-emphasis text-center text-sm not-italic font-light leading-[normal] font-inter">
                                {{ placeType }}
                            </div>
                        </div>
                        <!-- Divider -->
                        <div class="h-px shrink-0 self-stretch opacity-60 bg-medium-emphasis"></div>
                        <!-- Input -->
                        <div class="flex flex-col items-start gap-8 flex-[1_0_0] self-stretch">
                            <!-- Stars -->
                            <div class="flex items-start self-stretch">
                                <!-- Label -->
                                <div class="flex h-6 items-center flex-[1_0_0]">
                                    <div
                                        class="text-medium-emphasis font-inter text-base not-italic font-light leading-[normal]">
                                        Experience
                                    </div>
                                </div>
                                <!-- Rating -->
                                <div class="flex w-[152px] h-6 items-start gap-2 relative">
                                    <Button text rounded @click="submitRating(1)">
                                        <template #icon>
                                            <BaseIcon icon="star" :fill="rating >= 1 ? '#B1BF41' : 'none'"
                                                class="w-6 h-6 shrink-0 " />
                                        </template>
                                    </Button>
                                    <Button text rounded @click="submitRating(2)">
                                        <template #icon>
                                            <BaseIcon icon="star" :fill="rating >= 2 ? '#B1BF41' : 'none'"
                                                class="w-6 h-6 shrink-0 " />
                                        </template>
                                    </Button>
                                    <Button text rounded @click="submitRating(3)">
                                        <template #icon>
                                            <BaseIcon icon="star" :fill="rating >= 3 ? '#B1BF41' : 'none'"
                                                class="w-6 h-6 shrink-0 " />
                                        </template>
                                    </Button>
                                    <Button text rounded @click="submitRating(4)">
                                        <template #icon>
                                            <BaseIcon icon="star" :fill="rating >= 4 ? '#B1BF41' : 'none'"
                                                class="w-6 h-6 shrink-0 " />
                                        </template>
                                    </Button>
                                    <Button text rounded @click="submitRating(5)">
                                        <template #icon>
                                            <BaseIcon icon="star" :fill="rating >= 5 ? '#B1BF41' : 'none'"
                                                class="w-6 h-6 shrink-0 " />
                                        </template>
                                    </Button>
                                    <!-- Error message for rating -->
                                    <div v-if="!ratingValid"
                                        class="text-error text-[10px] not-italic font-light leading-[normal] font-inter absolute bottom-[-20px]">
                                        Please select the rating
                                    </div>
                                </div>
                            </div>
                            <!-- Text area -->
                            <div class="flex flex-col items-start gap-1 flex-[1_0_0] self-stretch">
                                <Textarea v-model="reviewText" type="text"
                                    placeholder="Share details of your experience"
                                    class="self-stretch text-base not-italic font-light leading-[normal]" rows="4" />
                                <!-- Error message for review text -->
                                <div v-if="!textValid"
                                    class="text-error text-[10px] not-italic font-light leading-[normal] font-inter">
                                    Your text must contain more than 5 and less than 200 words
                                </div>
                            </div>

                            <div
                                class="text-medium-emphasis font-inter text-base not-italic font-light leading-[normal]">
                                Images
                            </div>
                            <div class="relative w-full">
                                <FileUpload v-model="reviewPicture"> </FileUpload>
                            </div>
                        </div>

                        <!-- Divider -->
                        <div class="h-px shrink-0 self-stretch opacity-60 bg-medium-emphasis"></div>


                        <!-- Footer -->
                        <div class="flex justify-end items-start self-stretch">

                            <!-- Cancel button -->
                            <div class="flex justify-center items-center  px-2 py-1">
                                <Button outlined rounded label="Cancel" @click="closeModal"></Button>
                            </div>

                            <!-- Post button -->
                            <div class="flex justify-center items-center px-2 py-1">
                                <Button rounded label="Post" :disabled="!checkInputValidity()"
                                    @click="createReview"></Button>
                            </div>
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
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import FloatLabel from 'primevue/floatlabel'
import IconField from 'primevue/iconfield'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import { computed, ref, watch } from 'vue'
import DecoStrip from '@/components/DecoStrip.vue'
import { useAuthStore } from '@/stores/auth'
import FileUpload from '@/components/FileUpload.vue'
import { reviewService } from '@/services/reviewService'
import Textarea from 'primevue/textarea';

const authStore = useAuthStore()

const signedInUser = ref<User>(authStore.user)
const myId = ref<string>(signedInUser?.value.id)


const placeName = ref<string>('Restaurant Traube')
const placeType = ref<string>('Restaurant')
const rating = ref<number>(0)
const reviewText = ref<string>('')
const showModal = ref<boolean>(false)
const ratingValid = ref<boolean>(false)
const textValid = ref<boolean>(false)
const location = ref({
    id: 'placeholderId',
    name: 'Placeholder Location',
    coordinates: { x: '0', y: '0' }
});

const reviewPicture = ref<File | null>(null)

watch(reviewText, (newValue) => {
    const reviewTextWords = newValue.trim().split(/\s+/).length
    const reviewTextValue = newValue.trim()
    if (reviewTextWords > 5 && reviewTextWords < 200 && reviewTextValue !== '') {
        textValid.value = true
    } else {
        textValid.value = false
    }
})

watch(rating, (newValue) => {
    const ratingValue = parseInt(newValue);
    if (ratingValue > 0) {
        ratingValid.value = true;
    } else {
        ratingValid.value = false;
    }
});

const submitRating = (selectedRating: number) => {
    rating.value = selectedRating;
}

const openModal = () => {
    showModal.value = true;
    rating.value = 0 // Reset rating when modal is opened
    reviewText.value = ''
}

const closeModal = () => {
    showModal.value = false;
}
const openImageInput = () => {
    // Trigger file input click
    const fileInput = document.getElementById('fileInput') as HTMLInputElement
    fileInput.click()
}

const handleImageUpload = (event: Event) => {
    const file = (event.target as HTMLInputElement).files?.[0]
    // Handle the file upload
}

const checkInputValidity = () => {
    const reviewTextWords = reviewText.value.trim().split(/\s+/).length;
    const reviewTextValue = reviewText.value.trim();
    const ratingValue = parseInt(rating.value);

    if (reviewTextWords > 5 && reviewTextWords < 200 && reviewTextValue !== '') {
        textValid.value = true
    }
    if (ratingValue > 0) ratingValid.value = true
    return ratingValid.value && textValid.value
}

const createReview = async () => {
    if (checkInputValidity()) {
        try {
            console.log(location.value.coordinates.x)
            // Call createReview method from reviewService
            await reviewService.createReview(reviewText.value, rating.value, location.value)
            // Close modal after successful review creation
            await updateReviewImage()
            closeModal()
        } catch (error) {
            console.error('Error creating review:', error)
        }
    }
}

const updateReviewImage = async () => {

    const myReviews = ref<Review[]>()
    try {
        myReviews.value = await reviewService.getReviewsOfUser(myId.value)
    } catch (error) {
        console.error('Error accessing the created reviews:', error)
    }

    try {
        await reviewService.updateReviewImage(myReviews.value.reviews[0].review_id, reviewPicture)
    } catch (error) {
        console.error('Error updating review image:', error)
    }
}


</script>
