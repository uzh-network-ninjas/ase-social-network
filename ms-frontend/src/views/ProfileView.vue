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
                    <Button text rounded class="w-6 h-6" @click=$router.go(-1)>
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
                            {{ user?.username }}
                        </div>

                        <!--Stats-->
                        <div class="flex justify-center items-center gap-8">

                            <!--Review count-->
                            <div class="flex flex-col justify-center items-start">
                                <div
                                    class="self-stretch text-[color:var(--text-high-emphasis,rgba(0,0,0,0.89))] text-center text-2xl not-italic font-light leading-[normal]">
                                    {{ user?.reviews }}
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
                                    {{ user?.followers.length }}
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
                                    {{ user?.following.length }}
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
                                <Button rounded :label="followButtonText" iconPos="left" @click="toggleFollow">
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
        </main>
        <DecoStrip class="fixed bottom-0 right-1/4 top-0 z-50 max-lg:invisible lg:visible" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import Button from 'primevue/button'
import BaseIcon from '@/icons/BaseIcon.vue'
import { useRouter } from 'vue-router'
import { userService } from '@/services/userService'
import { User } from '@/types/User'

const router = useRouter()


const authStore = useAuthStore()

const userId = ref<string>('')
const user = ref<User>()

const profilePicUrl = ref<string>('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')

const isFollowing = ref<boolean>(false)

const followButtonText = computed(() => {
    return isFollowing.value ? "Unfollow" : "Follow"
})

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
    userId.value = router.currentRoute.value.params.userId as string // Access userId from router
    try {
        user.value = await userService.getUser(userId.value)
    } catch (error) {
        console.error('Error fetching user profile:', error)
    }
})
</script>
