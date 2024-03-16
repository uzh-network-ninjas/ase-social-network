<script setup lang="ts">
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import IconField from 'primevue/iconfield'
import FloatLabel from 'primevue/floatlabel'
import Button from 'primevue/button'
import { ref } from 'vue'
import Checkbox from 'primevue/checkbox'
import Navbar, { type MenuOption } from '@/components/TopNav.vue'
import BaseIcon from '@/icons/BaseIcon.vue'

const topNavActions: MenuOption[] = [
  {
    labelKey: 'sign_up',
    to: '/sign-up'
  },
  {
    labelKey: 'sign_in',
    icon: 'arrow-left-end-on-rectangle',
    to: '/sign-in'
  }
]

const value = ref<string>('')
const boolValue = ref<boolean>(true)
const boolValue2 = ref<boolean>(false)

import { useRouter } from 'vue-router';

const router = useRouter();

const redirectToLogInPage = () => {
  router.push('/login');
};

</script>

<template>
  <header class="sticky top-0 z-40">
    <Navbar :actions="topNavActions" iconPos="right" />
  </header>
  <main class="m-8">

    <button @click="redirectToLogInPage">Go to Log In page</button>

    <FloatLabel>
      <InputText id="username" v-model="value" />
      <label for="username">Username</label>
    </FloatLabel>

    <FloatLabel>
      <IconField iconPosition="right">
        <InputText v-model="value"></InputText>
        <InputIcon>

        </InputIcon>
      </IconField>
      <label for="password">Password</label>
    </FloatLabel>

    <div class="my-1 flex w-fit flex-col gap-2">
      <Button>Sign In</Button>
      <Button outlined>Hello</Button>
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
