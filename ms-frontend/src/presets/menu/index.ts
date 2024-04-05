export default {
  root: {
    class: ['min-w-[12rem]', 'rounded-lg', 'p-2', 'bg-white', 'shadow-lg']
  },
  menu: {
    class: ['list-none']
  },
  menuitem: {
    class: [
      'text-medium-emphasis',
      'rounded-lg',
      'hover:bg-selection-indicator hover:bg-opacity-5',
      'cursor-pointer'
    ]
  },
  content: {
    class: ['relative', 'flex', 'items-center', 'py-2', 'px-4', 'gap-4']
  }
}
