/*
  Regex pattern that matches a string based on RFC5322.
  Source: https://emailregex.com/
 */
const re =
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

export const emailValidator = {
  /**
   * Validates a string depending on if it represents a valid email address or not.
   * @param email
   * @returns {true} if the string is a valid email address
   * @returns {false} if the string is an invalid email address
   */
  validate: function (email: string): boolean {
    return re.test(email)
  }
}
