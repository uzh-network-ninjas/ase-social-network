export class User {
  id: string
  username: string
  email: string
  createdAt: Date
  updatedAt: Date | null

  constructor(data: {
    id: string
    username: string
    email: string
    created_at: string
    updated_at: string | null
  }) {
    this.id = data.id
    this.username = data.username
    this.email = data.email
    this.createdAt = new Date(data.created_at)
    this.updatedAt = data.updated_at ? new Date(data.updated_at) : null
  }
}
