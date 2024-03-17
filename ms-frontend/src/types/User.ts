export class User {
  id: string
  username: string
  email: string
  preferences?: string[]

  constructor(data: { id: string; username: string; email: string; preferences?: string[] }) {
    this.id = data.id
    this.username = data.username
    this.email = data.email
    this.preferences = data.preferences
  }
}
