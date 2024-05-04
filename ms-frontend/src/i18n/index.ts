import { createI18n } from 'vue-i18n'

import de from './de.json'
import en from './en.json'

export enum Locales {
  DE = 'de',
  EN = 'en'
}

const messages = {
  [Locales.DE]: de,
  [Locales.EN]: en
}

const savedLanguage = localStorage.getItem('selectedLanguage')
let selectedLanguage: Locales
if (
  savedLanguage &&
  Object.values(Locales)
    .map((value) => value.toString())
    .includes(savedLanguage)
) {
  selectedLanguage = Object.values(Locales).find((value) => value.toString() === savedLanguage)!
} else {
  selectedLanguage =
    Object.values(Locales).find((value) => navigator.language.includes(value.toString())) ??
    Locales.EN
}

export const i18n = createI18n({
  legacy: false,
  messages,
  locale: selectedLanguage,
  fallbackLocale: Locales.EN
})
