export class User {
  id: string
  image: string | null
  username: string
  email: string
  preferences?: string[]
  followers: User[]
  following: User[]

  constructor(data: {
    id: string
    username: string
    email: string
    preferences?: string[]
    followers: User[]
    following: User[]
  }) {
  preferences: string[]
  restrictions: string[]

  constructor(data: {
    id: string
    image: string | null
    username: string
    email: string
    preferences: string[]
    restrictions: string[]
  }) {
    this.id = data.id
    this.image = data.image
    this.username = data.username
    this.email = data.email
    this.preferences = data.preferences
    this.restrictions = data.restrictions
    this.followers = data.followers
    this.following = data.following
    this.image = data.image
  }
}
