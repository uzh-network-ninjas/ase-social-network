import type { TextareaProps, TextareaContext } from 'primevue/textarea'

export default {
  root: ({ props, context }: { props: TextareaProps; context: TextareaContext; parent: any }) => ({
    class: [
      'px-4',
      'py-3',
      'border',
      'rounded-lg',
      'text-base',
      'outline-none',

      { 'focus-visible:border-primary': !props.invalid && !context.disabled },

      {
        'border-medium-emphasis': !props.invalid && !context.disabled,
        'border-error': props.invalid && !context.disabled
      },
      { 'border-disabled': context.disabled },

      { 'text-disabled': context.disabled },
      { 'text-medium-emphasis': !context.disabled },

      // State for Wrappers
      { 'wrapper-info-filled': context.filled },
      { 'wrapper-info-disabled': context.disabled },
      { 'wrapper-info-invalid': props.invalid }
    ]
  })
}
