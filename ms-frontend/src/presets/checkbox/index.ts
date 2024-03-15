import type { CheckboxContext, CheckboxProps } from 'primevue/checkbox'

export default {
  root: {
    class: [
      'relative',
      'inline-flex',
      'justify-center',
      'items-center',
      'outlined-none',

      'w-6',
      'h-6'
    ]
  },
  box: ({ props, context }: { props: CheckboxProps; context: CheckboxContext }) => ({
    class: [
      'flex',
      'items-center',
      'justify-center',

      'w-5',
      'h-5',

      'rounded',
      'border',
      'ring-offset-1',
      { 'peer-focus-visible:ring-1': !context.disabled },
      {
        'border-medium-emphasis peer-hover:border-high-emphasis peer-hover:ring-high-emphasis  ring-medium-emphasis':
          !context.disabled && !props.invalid && !context.checked,
        'border-primary bg-primary peer-hover:bg-opacity-89 ring-primary peer-hover:ring-primary/89':
          !context.disabled && !props.invalid && context.checked
      },
      {
        'border-error peer-hover:border-error/89 ring-error peer-hover:ring-error/89':
          !context.disabled && props.invalid && !context.checked,
        'border-error bg-error peer-hover:bg-opacity-89 ring-error peer-hover:ring-error/89':
          !context.disabled && props.invalid && context.checked
      },

      'peer-disabled:opacity-38'
    ]
  }),
  input: {
    class: [
      'peer',

      'absolute',
      'top-1/2 left-1/2',
      '-translate-x-1/2',
      '-translate-y-1/2',
      'z-10',

      'w-5 h-5',
      'border',
      'rounded-lg',
      'opacity-0'
    ]
  },
  icon: {
    class: ['w-3', 'h-3', 'text-white']
  }
}
