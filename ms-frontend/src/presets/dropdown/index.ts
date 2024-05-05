import type { DropdownContext, DropdownProps, DropdownState } from 'primevue/dropdown'

type options = {
  props: DropdownProps
  state: DropdownState
  context: DropdownContext
}

export default {
  root: ({ props, state }: options) => ({
    class: [
      'inline-flex',
      'relative',
      'gap-3',

      'rounded-lg',
      'outline-none',
      'font-light',
      'border',

      { 'focus-within:border-primary': !props.disabled && !props.invalid },
      { 'border-medium-emphasis': !props.disabled && !props.invalid },
      { 'border-disabled': props.disabled && !props.invalid },
      { 'border-error': !props.disabled && props.invalid },

      'py-3',
      'px-4',

      { 'cursor-pointer': !props.disabled },
      { 'wrapper-info-filled': props.modelValue !== undefined || state.overlayVisible },
      { 'wrapper-info-disabled': props.disabled },
      { 'wrapper-info-invalid': props.invalid }
    ]
  }),
  input: {
    class: [
      'text-base',

      'flex-auto',

      'focus:outline-none',

      'text-medium-emphasis',

      'overflow-hidden overflow-ellipsis',
      'whitespace-nowrap',
      'appearance-none'
    ]
  },
  trigger: ({ state }: options) => ({
    class: [
      'flex items-center justify-center',

      'text-medium-emphasis',
      'transition-transform',
      'duration-150',
      { 'rotate-180': state.overlayVisible }
    ]
  }),
  panel: {
    class: ['absolute top-0 left-0', 'rounded-lg', 'shadow-lg', 'bg-background']
  },
  wrapper: {
    class: ['max-h-[200px]', 'overflow-auto']
  },
  list: {
    class: 'p-2 list-none flex flex-col gap-2'
  },
  item: ({ context }: options) => ({
    class: [
      'text-base',
      'text-medium-emphasis',
      'font-light',
      'px-4',
      'py-2',
      'rounded-lg',

      { 'bg-selection-indicator bg-opacity-5': context.focused && !context.selected },
      { 'bg-primary bg-opacity-35': context.focused && context.selected },

      { 'bg-primary bg-opacity-15': !context.focused && context.selected },

      { 'pointer-events-none cursor-default': context.disabled },
      { 'cursor-pointer': !context.disabled },
      'overflow-hidden',
      'whitespace-nowrap'
    ]
  }),
  transition: {
    enterFromClass: 'opacity-0 scale-y-[0.8]',
    enterActiveClass:
      'transition-[transform,opacity] duration-[120ms] ease-[cubic-bezier(0,0,0.2,1)]',
    leaveActiveClass: 'transition-opacity duration-100 ease-linear',
    leaveToClass: 'opacity-0'
  },
  emptymessage: {
    class: ['px-4', 'py-2', 'rounded-lg', 'text-medium-emphasis', 'text-base']
  }
}
