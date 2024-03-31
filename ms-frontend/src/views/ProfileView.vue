<template>
    <div>
        <header class="sticky top-0 z-40">
            <Navbar :actions="topNavActions" iconPos="right" />
        </header>
        <main class="md:pl-16">

            <!--Page title and back button-->
            <div class="flex items-center gap-4 self-stretch p-4">
                <div class="flex items-center gap-4 flex-[1_0_0]">

                    <!--Back button-->
                    <Button text rounded class="w-6 h-6">
                        <template #icon>
                            <BaseIcon icon="back" />
                        </template>
                    </Button>

                    <!--Name of the page-->
                    <div class="text-2xl not-italic font-extralight leading-[normal] font-inter text-medium-emphasis">
                        Profile
                    </div>





                </div>
                <Button text rounded class="flex justify-center items-center gap-3 p-1.5 rounded-lg">
                    <template #icon>
                        <BaseIcon icon="three-dots" />
                    </template>
                </Button>

            </div>

            <div class="flex flex-col items-center gap-8 flex-[1_0_0] self-stretch px-0 py-8">

                <!--Profile information-->
                <div class="flex justify-center items-start gap-8 self-stretch px-8 py-0">

                    <!-- Profile picture with masked green rectangle -->
                    <div class="flex w-[136px] h-[136px] justify-center items-center rounded-[128px] relative">
                        <!-- Green rectangle with rotation -->
                        <div class="w-[67.951px] h-[177.361px] absolute rotate-[-47.552deg] bg-primary overflow-hidden"
                            style="clip-path: circle(50.5%);"></div>
                        <div class="w-[132px] h-[132px] absolute rounded-[128px] left-0.5 top-0.5 bg-white"></div>
                        <!-- Profile picture -->
                        <img :src="profilePicUrl" alt="Profile Picture"
                            class="w-32 h-32 shrink-0 rounded-[128px] bg-cover bg-no-repeat bg-center bg-lightgray z-10" />
                    </div>



                    <!--Information-->
                    <div class="flex flex-col items-start gap-4 flex-[1_0_0]">

                        <!--Username-->
                        <div
                            class="text-[color:var(--secondary-color,#5C917F)] text-center text-2xl not-italic font-light leading-[normal]">
                            {{ username }}
                        </div>

                        <!--Stats-->
                        <div class="flex justify-center items-center gap-8">

                            <!--Review count-->
                            <div class="flex flex-col justify-center items-start">
                                <div
                                    class="self-stretch text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))] text-center text-2xl not-italic font-light leading-[normal]">
                                    {{ uploadedReviewsCount }}
                                </div>
                                <div
                                    class="self-stretch text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))] text-center text-base not-italic font-light leading-[normal]">
                                    Reviews
                                </div>
                            </div>

                            <!--Divider-->
                            <div class="opacity-30 w-px self-stretch bg-medium-emphasis"></div>

                            <!--Follower count-->
                            <div class="flex flex-col justify-center items-start">
                                <div
                                    class="self-stretch text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))] text-center text-2xl not-italic font-light leading-[normal]">
                                    {{ followersCount }}
                                </div>
                                <div
                                    class="self-stretch text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))] text-center text-base not-italic font-light leading-[normal]">
                                    Followers
                                </div>
                            </div>

                            <!--Divider-->
                            <div class="opacity-30 w-px self-stretch bg-medium-emphasis"></div>

                            <!--Follows count-->
                            <div class="flex flex-col justify-center items-start">
                                <div
                                    class="self-stretch text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))] text-center text-2xl not-italic font-light leading-[normal]">
                                    {{ followsCount }}
                                </div>
                                <div
                                    class="self-stretch text-[color:var(--text-medium-emphasis,rgba(0,0,0,0.60))] text-center text-base not-italic font-light leading-[normal]">
                                    Follows
                                </div>
                            </div>
                        </div>

                        <!--Actions-->
                        <div class="flex justify-center items-start gap-8">

                            <!--Follow button-->
                            <div class="flex justify-center items-center gap-2 px-4 py-1">
                                <Button rounded label="Follow" iconPos="left">
                                    <template #icon>
                                        <BaseIcon icon="user-plus" />
                                    </template>
                                </Button>
                            </div>

                            <!--Share button-->
                            <div class="flex justify-center items-center gap-3 px-4 py-1">
                                <Button outlined rounded label="Share" iconPos="left">
                                    <template #icon>
                                        <BaseIcon icon="share" />
                                    </template>
                                </Button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <!-- <div class="mx-4 flex h-full items-center justify-center pt-8 md:justify-start">
                <div class="flex flex-col gap-8">
                    <h1
                        class="text-center text-2xl font-light uppercase tracking-widest text-secondary md:text-start md:text-5xl">
                        {{ $t('profile') }}
                    </h1>

                    <div class="profile-header">
                        <img :src="profilePicUrl" alt="Profile Picture" class="profile-picture" />
                        <h1>{{ username }}</h1>
                        <div class="profile-stats">
                            <div>{{ uploadedReviewsCount }} Reviews</div>
                            <div>{{ followersCount }} Followers</div>
                            <div>{{ followsCount }} Follows</div>
                        </div>
                        <button @click="toggleFollow" class="follow-button">{{ isFollowing ? $t('unfollow') :
                            $t('follow') }}</button>
                    </div>
                </div>
            </div> -->
        </main>
        <DecoStrip class="fixed bottom-0 right-1/4 top-0 z-50 max-lg:invisible lg:visible" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import Button from 'primevue/button'
import BaseIcon from '@/icons/BaseIcon.vue'
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import FloatLabel from 'primevue/floatlabel'
import IconField from 'primevue/iconfield'

const authStore = useAuthStore()

const profilePicUrl = ref<string>('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')
const username = ref<string>('username')

// Mock data for demonstration, replace with actual data retrieval
const uploadedReviewsCount = ref<number>(10)
const followersCount = ref<number>(12)
const followsCount = ref<number>(50)

const isFollowing = ref<boolean>(false)

// Function to toggle follow status
const toggleFollow = () => {
    isFollowing.value = !isFollowing.value
    // Perform actual follow/unfollow action here
}

const topNavActions: MenuOption[] = [
    {
        labelKey: 'sign_out',
        icon: 'log-out',
        to: '/sign-out'
    }
]

// Fetch user profile data on component mount
onMounted(async () => {
    // Fetch user profile data from API or store
    // Set profilePicUrl and username accordingly
})
</script>
