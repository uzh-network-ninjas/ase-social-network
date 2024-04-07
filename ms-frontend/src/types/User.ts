export class User {
  id: string
  username: string
  email: string
  preferences?: string[]
  followers: User[]
  following: User[]
  image?: File

  constructor(data: {
    id: string
    username: string
    email: string
    preferences?: string[]
    followers: User[]
    following: User[]
    image?: File
  }) {
    this.id = data.id
    this.username = data.username
    this.email = data.email
    this.preferences = data.preferences
    this.followers = data.followers
    this.following = data.following
    this.image = data.image
  }
}
