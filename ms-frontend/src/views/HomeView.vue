<script setup lang="ts">
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import IconField from 'primevue/iconfield'
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'
import FloatLabel from 'primevue/floatlabel'
import Button from 'primevue/button'
import { ref } from 'vue'
import Checkbox from 'primevue/checkbox'

const value = ref<string>('')
const boolValue = ref<boolean>(true)
const boolValue2 = ref<boolean>(false)
</script>
<template>
  <main class="m-8">
    <FloatLabel>
      <IconField iconPosition="right">
        <InputIcon>
          <MagnifyingGlassIcon></MagnifyingGlassIcon>
        </InputIcon>
        <InputText v-model="value"></InputText>
      </IconField>
      <label for="username">Username</label>
    </FloatLabel>
    <div class="my-1 flex w-fit flex-col gap-2">
      <Button>Button</Button>
      <Button outlined>Hello</Button>
      <Button text>Hello</Button>
      <Button rounded>Button</Button>
      <Button outlined rounded>Hello</Button>
      <Button text rounded>Hello</Button>
      <Button rounded disabled>Button</Button>
      <Button outlined rounded disabled>Hello</Button>
      <Button rounded label="Hello" iconPos="right">
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Button outlined rounded label="Hello">
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Button text rounded label="Hello">
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Button rounded>
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Button outlined rounded>
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Button text rounded>
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Button label="Link" link disabled />
      <Button label="Link" link />
      <Button label="Link" link>
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>
      <Checkbox v-model="boolValue" binary />
      <Checkbox v-model="boolValue2" binary />
      <Checkbox v-model="boolValue2" invalid binary />
      <Checkbox disabled binary />
    </div>
  </main>
</template>
