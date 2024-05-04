import { Loader } from '@googlemaps/js-api-loader'

const loader = new Loader({
  apiKey: import.meta.env.VITE_GOOGLE_API_KEY,
  libraries: ['places'],
  language: navigator.language
})

const autocompleteService: google.maps.places.AutocompleteService = await loader
  .importLibrary('places')
  .then(({ AutocompleteService }) => {
    return new AutocompleteService()
  })

const MarkerLibraryType: google.maps.MarkerLibrary = await loader
  .importLibrary('marker')
  .then((MarkerLibrary: google.maps.MarkerLibrary) => {
    return MarkerLibrary
  })

export { loader, autocompleteService, MarkerLibraryType }
