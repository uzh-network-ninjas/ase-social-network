import type { IconFieldProps } from 'primevue/iconfield'

export default {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  root: ({ props }: { props: IconFieldProps }) => ({
    class: [
      'relative',
      '[&>input]:w-full',
      '[&>*:first-child]:absolute',
      '[&>*:first-child]:top-1/2',
      '[&>*:first-child]:-translate-y-1/2',
      '[&>*:first-child]:text-medium-emphasis',
      {
        '[&>*:first-child]:right-3': props.iconPosition === 'right',
        '[&>*:first-child]:left-3': props.iconPosition === 'left'
      },
      {
        '[&>*:last-child]:pr-10': props.iconPosition === 'right',
        '[&>*:last-child]:pl-10': props.iconPosition === 'left'
      },
      '[&>*:first-child]:has-[.wrapper-info-disabled]:text-disabled'
    ]
  })
}
