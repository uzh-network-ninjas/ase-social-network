<script setup lang="ts">
import { ref } from 'vue'
import Dropdown from 'primevue/dropdown'
import FloatLabel from 'primevue/floatlabel'
import MiniChevronDown from '@/icons/MiniChevronDownIcon.vue'
import InputText from 'primevue/inputtext'
import Checkbox from 'primevue/checkbox'
import BaseIcon from '@/icons/BaseIcon.vue'
import InputIcon from 'primevue/inputicon'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import ToggleButton from 'primevue/togglebutton'
import AutoComplete from 'primevue/autocomplete'

const value = ref<string>('')
const boolValue = ref<boolean>(true)
const boolValue2 = ref<boolean>(false)

const selectedOption = ref()
const options = ref([
  { name: 'Option 1' },
  { name: 'Option 2' },
  { name: 'Option 3' },
  { name: 'Option 4' },
  { name: 'Option 5' }
])

const checked = ref<boolean>(false)

const autocomplete = ref<string>('')
const items = ref<string[]>([])

const search = (event: any) => {
  items.value = [...Array(10).keys()].map((item) => event.query + '-' + item)
}
</script>

<template>
  <main class="m-8">
    <FloatLabel class="mt-4 w-full">
      <Dropdown v-model="selectedOption" :options="options" optionLabel="name" class="w-full">
        <template #dropdownicon>
          <MiniChevronDown />
        </template>
      </Dropdown>
      <label for="dd-city">Select an Option</label>
    </FloatLabel>

    <FloatLabel class="mt-4 w-full">
      <Dropdown
        v-model="selectedOption"
        :options="options"
        optionLabel="name"
        class="w-full"
        disabled
      >
        <template #dropdownicon>
          <MiniChevronDown />
        </template>
      </Dropdown>
      <label for="dd-city">Select an Option</label>
    </FloatLabel>

    <FloatLabel class="mt-4 w-full">
      <Dropdown
        v-model="selectedOption"
        :options="options"
        optionLabel="name"
        class="w-full"
        invalid
      >
        <template #dropdownicon>
          <MiniChevronDown />
        </template>
      </Dropdown>
      <label for="dd-city">Select an Option</label>
    </FloatLabel>

    <Dropdown :options="[]" optionLabel="name" class="mt-4 w-full">
      <template #dropdownicon>
        <MiniChevronDown />
      </template>
    </Dropdown>

    <Dropdown
      v-model="selectedOption"
      :options="options"
      optionLabel="name"
      class="mt-4 border-none"
    >
      <template #dropdownicon>
        <MiniChevronDown />
      </template>
    </Dropdown>

    <FloatLabel class="mt-4">
      <InputText id="username" v-model="value" />
      <label for="username">Username</label>
    </FloatLabel>

    <FloatLabel class="mt-4">
      <InputText id="username" v-model="value" disabled />
      <label for="username">Username</label>
    </FloatLabel>

    <FloatLabel class="mt-4">
      <InputText id="username" v-model="value" invalid />
      <label for="username">Username</label>
    </FloatLabel>

    <FloatLabel class="mt-4">
      <IconField iconPosition="right">
        <InputText v-model="value"></InputText>
        <InputIcon> </InputIcon>
      </IconField>
      <label for="password">Password</label>
    </FloatLabel>

    <div class="mt-4 flex w-fit flex-col gap-2">
      <AutoComplete v-model="autocomplete" :suggestions="items" @complete="search"></AutoComplete>
      <AutoComplete
        v-model="autocomplete"
        :suggestions="items"
        @complete="search"
        variant="filled"
      ></AutoComplete>
      <AutoComplete
        v-model="autocomplete"
        :suggestions="items"
        @complete="search"
        disabled
      ></AutoComplete>
      <AutoComplete
        v-model="autocomplete"
        :suggestions="items"
        @complete="search"
        invalid
      ></AutoComplete>

      <ToggleButton v-model="checked" onLabel="Ascending" offLabel="Descending">
        <template #icon="propScope">
          <BaseIcon :icon="propScope.value ? 'arrow-up' : 'arrow-down'" :stroke-width="1.5" />
        </template>
      </ToggleButton>

      <ToggleButton v-model="checked" onLabel="Ascending" offLabel="Descending" class="border-none">
        <template #icon="propScope">
          <BaseIcon :icon="propScope.value ? 'arrow-up' : 'arrow-down'" :stroke-width="1.5" />
        </template>
      </ToggleButton>

      <ToggleButton v-model="checked" onLabel="Ascending" offLabel="Descending" invalid>
        <template #icon="propScope">
          <BaseIcon :icon="propScope.value ? 'arrow-up' : 'arrow-down'" :stroke-width="1.5" />
        </template>
      </ToggleButton>

      <ToggleButton v-model="checked" onLabel="Ascending" offLabel="Descending" disabled>
        <template #icon="propScope">
          <BaseIcon :icon="propScope.value ? 'arrow-up' : 'arrow-down'" :stroke-width="1.5" />
        </template>
      </ToggleButton>

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
