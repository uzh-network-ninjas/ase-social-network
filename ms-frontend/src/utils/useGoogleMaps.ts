import { Loader } from '@googlemaps/js-api-loader'

let autocompleteService: google.maps.places.AutocompleteService
let MarkerLibraryType: google.maps.MarkerLibrary

const loader = new Loader({
  apiKey: import.meta.env.VITE_GOOGLE_API_KEY,
  libraries: ['places'],
  language: 'de'
})

await loader.importLibrary('places').then(({ AutocompleteService }) => {
  autocompleteService = new AutocompleteService()
})

await loader.importLibrary('marker').then((MarkerLibrary: google.maps.MarkerLibrary) => {
  MarkerLibraryType = MarkerLibrary
})

export { loader, autocompleteService, MarkerLibraryType }
