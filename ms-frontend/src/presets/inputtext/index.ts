import type { InputTextProps, InputTextContext } from 'primevue/inputtext'
export default {
  root: ({
    props,
    context
  }: {
    props: InputTextProps
    context: InputTextContext
    parent: any
  }) => ({
    class: [
      'px-4',
      props.variant == 'filled' ? 'py-2' : 'py-3',
      { border: props.variant != 'filled' },
      'rounded-lg',
      'text-base',
      'font-light',
      'outline-none',
      { 'bg-selection-indicator/5': props.variant == 'filled' },

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
