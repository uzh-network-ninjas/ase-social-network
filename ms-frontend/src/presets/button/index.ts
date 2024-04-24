import type { ButtonContext, ButtonProps } from 'primevue/button'
import Button from 'primevue/button'

export default {
  root: ({
    instance,
    props,
    context
  }: {
    instance: Button
    props: ButtonProps
    context: ButtonContext
    parent: any
  }) => ({
    class: [
      'relative',
      'py-1',
      'outline-none',
      'ring-offset-1',
      'focus-visible:ring-1',
      'font-light',
      'inline-flex',
      'justify-center',
      'items-center',

      {
        '[&>*:last-child]:bg-white/50': !props.outlined && !props.text && !props.link
      },

      {
        'w-fit': instance.$slots.icon !== undefined,
        'gap-3': instance.$slots.icon !== undefined && props.label !== null
      },

      {
        'px-0': props.link,
        'px-4': props.label != null && !props.text && !props.link,
        'px-2': props.label != null && props.text,
        'px-1.5': instance.$slots.icon !== undefined && props.label == null
      },

      {
        'flex-row': props.iconPos == 'left',
        'flex-row-reverse': props.iconPos == 'right',
        'flex-col': props.iconPos == 'top',
        'flex-col-reverse': props.iconPos == 'bottom'
      },

      { border: !props.text && !props.link },

      { 'ring-primary': !props.text && !props.outlined },
      { 'ring-medium-emphasis': props.outlined || props.text },

      { 'bg-primary': !props.outlined && !props.text && !props.link },
      { 'bg-background': props.outlined || props.link },

      { 'text-contrast': !props.outlined && !props.text && !props.link },
      { 'text-medium-emphasis': (props.outlined || props.text) && !context.disabled },
      { 'text-primary': props.link },

      { 'border-primary': !props.outlined && !props.text },
      { 'border-medium-emphasis': props.outlined && !context.disabled },

      { 'rounded-lg': props.rounded },

      { underline: props.link },

      { 'hover:bg-opacity-89': !props.outlined && !props.text && !props.link && !context.disabled },
      {
        'hover:ring-primary hover:border-primary hover:text-primary':
          props.outlined && !context.disabled
      },
      { 'hover:ring-primary hover:text-primary': props.text && !context.disabled },
      { 'hover:no-underline': props.link && !context.disabled },

      {
        'text-disabled border-disabled':
          (props.link || props.outlined || props.text) && context.disabled
      },
      { 'opacity-38': !props.outlined && !props.text && context.disabled }
    ]
  }),
  label: ({ props }: { props: ButtonProps }) => ({
    class: [{ 'w-0': props.label == null }]
  })
}
