import type { IconFieldProps } from 'primevue/iconfield'

export default {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  root: ({ props }: { props: IconFieldProps }) => ({
    class: [
      'relative',
      '[&>input]:w-full',
      '[&>*:last-child]:absolute',
      '[&>*:last-child]:top-1/2',
      '[&>*:last-child]:-translate-y-1/2',
      '[&>*:last-child]:text-medium-emphasis',
      {
        '[&>*:last-child]:right-3': props.iconPosition === 'right',
        '[&>*:last-child]:left-3': props.iconPosition === 'left'
      },
      {
        '[&>*:first-child]:pr-10': props.iconPosition === 'right',
        '[&>*:first-child]:pl-10': props.iconPosition === 'left'
      },
      {
        '[&>div:first-child>*:first-child]:pr-10': props.iconPosition === 'right',
        '[&>div:first-child>*:first-child]:pl-10': props.iconPosition === 'left'
      },
      '[&>*:last-child]:has-[.wrapper-info-disabled]:text-disabled',
      '[&>*:last-child]:has-[.wrapper-info-invalid]:text-error'
    ]
  })
}
