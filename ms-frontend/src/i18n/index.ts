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

export const i18n = createI18n({
  legacy: false,
  messages,
  locale: Locales.EN,
  fallbackLocale: Locales.EN
})
