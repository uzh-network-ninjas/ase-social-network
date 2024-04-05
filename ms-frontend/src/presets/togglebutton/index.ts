import type { ToggleButtonPassThroughMethodOptions } from 'primevue/togglebutton'

export default {
  root: ({ props }: ToggleButtonPassThroughMethodOptions) => ({
    class: [
      'relative',
      'group',

      'inline-flex',

      'rounded-lg',
      'border',
      { 'border-medium-emphasis': !props.disabled && !props.invalid },
      { 'border-disabled': props.disabled },
      { 'border-error/100 hover:border-error/60': props.invalid },

      'ring-offset-1',
      '[&:has(*:focus-visible)]:ring-1',
      { 'ring-medium-emphasis': !props.disabled && !props.invalid },
      { 'hover:ring-primary': !props.disabled && !props.invalid },
      { 'ring-error hover:ring-error/60': !props.disabled && props.invalid },

      { 'hover:border-primary': !props.disabled && !props.invalid },

      'select-none',

      { 'pointer-events-none': props.disabled }
    ]
  }),
  box: ({ props }: ToggleButtonPassThroughMethodOptions) => ({
    class: [
      'inline-flex flex-1 items-center justify-center gap-3',

      'h-8',

      'px-4 py-1',

      'rounded-lg',

      { 'text-medium-emphasis group-hover:text-primary': !props.disabled && !props.invalid },
      { 'text-disabled': props.disabled },
      { 'text-error group-hover:text-error/60': props.invalid },

      { 'group-hover:text-   primary': !props.disabled && !props.invalid }
    ]
  }),
  label: {
    class: ['text-center w-full']
  },
  input: ({ props }: ToggleButtonPassThroughMethodOptions) => ({
    class: [
      'w-full',
      'h-full',

      'absolute',
      'top-0, left-0',

      'p-0',
      'm-0',
      'z-10',

      'opacity-0',
      'rounded-lg',
      'outline-none',

      'appearance-none',
      {
        'cursor-pointer': !props.disabled,
        'pointer-events-none cursor-default': props.disabled
      }
    ]
  }),
  icon: {
    class: 'font-base'
  }
}
