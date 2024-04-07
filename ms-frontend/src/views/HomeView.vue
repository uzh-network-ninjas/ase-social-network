<script setup lang="ts">
import TopNav, { type MenuOption } from '@/components/TopNav.vue'
import { type IconType } from '@/icons/BaseIcon.vue'
import { useAuthStore } from '@/stores/auth'
import SignedInTopNav from '@/components/SignedInTopNav.vue'

const authStore = useAuthStore()
const router = useRouter()

const signedIn = authStore.signedIn
const name = authStore.user?.username ?? ''


const topNavActions: MenuOption[] = [
  {
    labelKey: 'sign_up',
    to: { name: 'sign-up' }
  },
  {
    labelKey: 'sign_in',
    icon: 'arrow-left-start-on-rectangle' as IconType,
    to: { name: 'sign-in' }
  }
]

const foundUser = ref<User | null>(null)
const searchUsername = ref<string>('')

// Function to find a user by username
async function findUserByUsername(username: string) {
  try {
    // Call the findUser method from the userService
    const user = await userService.findUser(username)
    foundUser.value = user
  } catch (error) {
    console.error('Error finding user:', error)
    foundUser.value = null
  }
}

// Function to navigate to the profile page with a specific userId
const navigateToProfilePage = (userId: string) => {
  router.push(`/profile/${userId}`)
}
</script>

<template>
  <header class="sticky top-0 z-40">
    <TopNav v-if="!authStore.signedIn" :actions="topNavActions" iconPos="right" />
    <SignedInTopNav v-else />
  </header>

  <main class="m-8">
    <div
      v-if="signedIn"
      class="text-center text-2xl font-light uppercase tracking-widest text-secondary md:text-start md:text-5xl"
    >
      Hello, {{ name }}!
      <!--Your id is {{ id }} -->
    </div>

    <!-- Search bar for username -->
    <div v-if="signedIn" class="flex items-center space-x-2">
      <input
        v-model="searchUsername"
        type="text"
        placeholder="Search by username"
        class="rounded-lg border border-gray-300 p-2 focus:border-primary focus:outline-none"
      />
      <button
        @click="findUserByUsername(searchUsername)"
        class="rounded-lg bg-primary px-4 py-2 text-white hover:bg-secondary focus:bg-blue-600 focus:outline-none"
      >
        Search
      </button>
    </div>

    <!-- Display button with found user's username -->
    <div v-if="foundUser" class="mt-4">
      <button
        @click="navigateToProfilePage(foundUser.id)"
        class="rounded-lg bg-primary px-4 py-2 text-white hover:bg-blue-600 focus:bg-blue-600 focus:outline-none"
      >
        {{ foundUser.username }}
      </button>
    </div>
  </main>
</template>
