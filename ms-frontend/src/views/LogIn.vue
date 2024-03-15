<script setup lang="ts">
import InputText from 'primevue/inputtext'
import InputIcon from 'primevue/inputicon'
import FloatLabel from 'primevue/floatlabel'
import { ref } from 'vue'
import Password from 'primevue/password';
import Menubar from 'primevue/menubar';
import Button from 'primevue/button';
import MagnifyingGlassIcon from '@/icons/MagnifyingGlassIcon.vue'

const username = ref<string>('')
const password = ref<string>('')

import { useRouter } from 'vue-router';

const router = useRouter();


</script>

<template>
    <main class="m-8">

        <Button text rounded label="Review App" style = "color: var(--primary-color, #B1BF41);
font-family: Inter;
font-size: 20px;
font-style: normal;
font-weight: 500;
line-height: normal;
letter-spacing: 5px;
text-transform: uppercase;">
        <template #icon>
          <MagnifyingGlassIcon />
        </template>
      </Button>

        <h1 style="color: var(--primary-color, #B1BF41);
                    font-family: Inter;
                    font-size: 20px;
                    font-style: normal;
                    font-weight: 500;
                    line-height: normal;
                    letter-spacing: 5px;
                    text-transform: uppercase;">Review App</h1>

        <h1 style=" color: var(--secondary-color, #5C917F); font-family: Inter; font-size: 48px; font-style: normal;
            font-weight: 300; line-height: normal; letter-spacing: 12px; text-transform: uppercase;">SIGN IN</h1>

        <div class="my-1 flex w-fit flex-col gap-2">
            <FloatLabel>
                <InputText id=" username" v-model="value" />
                <label for="username">Username</label>
            </FloatLabel>

            <FloatLabel>
                <Password v-model="password" :feedback="false" inputId="password" toggleMask />
                <label for="password">Password</label>
            </FloatLabel>

            <Button label="Forgot your password?" link />
            <Button rounded>Sign In</Button>

            <Button label="Don't have an account yet? Register" link />


        </div>
    </main>
</template>
