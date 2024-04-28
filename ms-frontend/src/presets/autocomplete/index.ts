import type { AutoCompletePassThroughMethodOptions } from 'primevue/autocomplete'

export default {
  root: () => ({
    class: ['relative', 'inline-flex', 'w-full']
  }),
  input: ({ props }: AutoCompletePassThroughMethodOptions) => ({
    class: [
      'px-4',
      'w-full',
      props.variant == 'filled' ? 'py-2' : 'py-3',
      { border: props.variant != 'filled' },
      'rounded-lg',
      'text-base',
      'font-light',
      'outline-none',
      { 'bg-selection-indicator/5': props.variant == 'filled' },
      { 'focus-visible:border-primary': !props.invalid && !props.disabled },

      {
        'border-medium-emphasis': !props.invalid && !props.disabled,
        'border-error': props.invalid && !props.disabled
      },
      { 'border-disabled': props.disabled },

      { 'text-disabled': props.disabled },
      { 'text-medium-emphasis': !props.disabled }
    ]
  }),
  loadingicon: {
    class: ['text-medium-emphasis', 'absolute right-10 top-1/3 animate-spin']
  },
  panel: {
    class: [
      'absolute top-0 left-0',
      'rounded-lg',
      'shadow-lg',
      'bg-background',
      'max-h-[200px] max-w-full overflow-auto'
    ]
  },
  list: {
    class: 'p-2 list-none flex flex-col gap-2'
  },
  item: ({ context }: AutoCompletePassThroughMethodOptions) => ({
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
      { 'cursor-pointer': !context.disabled },
      { 'pointer-events-none cursor-default': context.disabled },
      'overflow-hidden',
      'whitespace-nowrap'
    ]
  }),
  emptymessage: {
    class: ['px-4', 'py-2', 'rounded-lg', 'text-medium-emphasis', 'text-base']
  },
  transition: {
    enterFromClass: 'opacity-0 scale-y-[0.8]',
    enterActiveClass:
      'transition-[transform,opacity] duration-[120ms] ease-[cubic-bezier(0,0,0.2,1)]',
    leaveActiveClass: 'transition-opacity duration-100 ease-linear',
    leaveToClass: 'opacity-0'
  }
}
