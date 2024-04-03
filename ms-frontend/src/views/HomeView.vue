<script setup lang="ts">
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import IconField from 'primevue/iconfield'
import FloatLabel from 'primevue/floatlabel'
import Button from 'primevue/button'
import { ref } from 'vue'
import Checkbox from 'primevue/checkbox'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import BaseIcon, { type IconType } from '@/icons/BaseIcon.vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { userService } from '@/services/userService'
import { User } from '@/types/User'


const authStore = useAuthStore()
const router = useRouter()

const signedIn = authStore.signedIn
console.log('signed in?: ', signedIn)
const name = authStore.user?.username ?? ''
console.log('username: ', name)
const id = authStore.user?.id ?? ''
const user = ref<User>()

// try {
//   const userData = await userService.getUser(id)
//   user.value = userData
// } catch (error) {
//   console.error('Error fetching user profile:', error)
// }


const value = ref<string>('')
const boolValue = ref<boolean>(true)
const boolValue2 = ref<boolean>(false)

const topNavActions: MenuOption[] = [
  ...(signedIn
    ? [
      {
        labelKey: 'sign_out',
        icon: 'arrow-left-end-on-rectangle' as IconType,
        before: () => {
          authStore.signOut()
        },
        to: { name: 'sign-in' }
      }
    ]
    : [
      {
        labelKey: 'sign_up',
        to: { name: 'sign-up' }
      },
      {
        labelKey: 'sign_in',
        icon: 'arrow-left-start-on-rectangle' as IconType,
        to: { name: 'sign-in' }
      }
    ])
]



// Function to navigate to the profile page with a specific userId
const navigateToProfilePage = (userId: string) => {
  router.push(`/profile/${userId}`)
}
</script>

<template>
  <header class="sticky top-0 z-40">
    <Navbar :actions="topNavActions" iconPos="right" />
  </header>

  <main class="m-8">
    <div v-if="signedIn"
      class="text-center text-2xl font-light uppercase tracking-widest text-secondary md:text-start md:text-5xl">
      Hello, {{ name }}!
    </div>

    <FloatLabel>
      <InputText id="username" v-model="value" />
      <label for="username">Username</label>
    </FloatLabel>

    <FloatLabel>
      <IconField iconPosition="right">
        <InputText v-model="value"></InputText>
        <InputIcon> </InputIcon>
      </IconField>
      <label for="password">Password</label>
    </FloatLabel>

    <div class="my-1 flex w-fit flex-col gap-2">
      <Button>Sign In</Button>
      <Button outlined @click="navigateToProfilePage(id)">{{ name }}</Button>
      <Button text>Hello</Button>
      <Button rounded>Button</Button>
      <Button outlined rounded>Hello</Button>
      <Button text rounded>Hello</Button>
      <Button rounded disabled>Button</Button>
      <Button outlined rounded disabled>Hello</Button>
      <Button rounded label="Hello" iconPos="right">
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Button outlined rounded label="Hello">
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Button text rounded label="Hello">
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Button rounded>
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Button outlined rounded>
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Button text rounded>
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Button label="Link" link disabled />
      <Button label="Link" link />
      <Button label="Link" link>
        <template #icon>
          <BaseIcon icon="magnifying-glass" />
        </template>
      </Button>
      <Checkbox v-model="boolValue" binary />
      <Checkbox v-model="boolValue2" binary />
      <Checkbox v-model="boolValue2" invalid binary />
      <Checkbox disabled binary />
    </div>
  </main>
</template>
