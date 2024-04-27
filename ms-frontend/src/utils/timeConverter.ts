const time_formats = [
  { cap: 60, unit: 1, singularKey: 'second', pluralKey: 'seconds' }, // cap: 60,                 unit: 1 sec (sec)
  { cap: 3600, unit: 60, singularKey: 'minute', pluralKey: 'minutes' }, // cap: 60*60,              unit: 60 sec (minute)
  { cap: 86400, unit: 3600, singularKey: 'hour', pluralKey: 'hours' }, // cap: 60*60*24,           unit: 60*60 sec (hour)
  { cap: 604800, unit: 86400, singularKey: 'day', pluralKey: 'days' }, // cap: 60*60*24*7,         unit: 60*60*60 sec (days)
  { cap: 2419200, unit: 604800, singularKey: 'week', pluralKey: 'weeks' }, // cap: 60*60*24*7*4,       unit: 60*60*24*7 sec (week)
  { cap: 29030400, unit: 2419200, singularKey: 'month', pluralKey: 'months' }, // cap: 60*60*24*7*4*12,    unit: 60*60*24*7*4 (month)
  { cap: 2903040000, unit: 29030400, singularKey: 'year', pluralKey: 'years' }, // cap: 60*60*24*7*4*12*10, unit: 60*60*24*7*4*12 (year)
  { cap: Number.MAX_SAFE_INTEGER, unit: 2903040000, singularKey: 'decade', pluralKey: 'decades' } // cap: infinite ,          unit: 60*60*24*7*4*12*10 (century)
]

export const TimeConverter = {
  humanReadable: function (date: Date): { key: string; value: number | undefined } {
    const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000)
    if (seconds == 0) {
      return { key: 'just_now', value: undefined }
    }

    const absSeconds = Math.abs(seconds)

    let key = ''
    let value: number | undefined
    for (let i = 0; i < time_formats.length; ++i) {
      if (absSeconds < time_formats[i].cap) {
        value = Math.floor(absSeconds / time_formats[i].unit)
        if (value < 2) {
          key += time_formats[i].singularKey
        } else {
          key += time_formats[i].pluralKey
        }
        break
      }
    }

    if (seconds > 0) {
      key += '_ago'
    } else {
      key += '_from_now'
    }

    return { key: key, value: value }
  }
}
