export default {
  root: {
    class: [
      'block relative font-light',
      '[&>input]:w-full',

      // Base Appearance
      '[&>*:last-child]:text-base',
      '[&>*:last-child]:absolute',
      '[&>*:last-child]:top-1/2',
      '[&>*:last-child]:-translate-y-1/2',
      '[&>*:last-child]:left-4',
      '[&>*:last-child]:pointer-events-none',
      '[&>*:last-child]:transition-all',
      '[&>*:last-child]:duration-200',
      '[&>*:last-child]:ease',
      '[&>*:last-child]:text-medium-emphasis',
      '[&>*:last-child]:px-1',
      '[&>*:first-child]:peer',

      // Override focus appearance if child is disabled
      '[&:has(.wrapper-info-disabled)>*:last-child]:top-1/2',
      '[&:has(.wrapper-info-disabled)>*:last-child]:text-base',

      // Focus Appearance
      '[&:focus-within>*:last-child]:-top-0',
      '[&:focus-within>*:last-child]:bg-background',
      '[&:focus-within>*:last-child]:text-primary',
      '[&:focus-within>*:last-child]:text-xs',

      '[&>*:last-child]:has-[.wrapper-info-filled]:-top-0',
      '[&>*:last-child]:has-[.wrapper-info-filled]:bg-background',
      '[&>*:last-child]:has-[.wrapper-info-filled]:text-xs',

      '[&>*:last-child]:has-[.border-error]:text-error',
      '[&>*:last-child]:has-[.wrapper-info-disabled]:text-disabled'
    ]
  }
}
