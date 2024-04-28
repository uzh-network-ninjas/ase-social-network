export class User {
  id: string
  image: string | null
  username: string
  email: string
  preferences: string[]
  restrictions: string[]
  followers: string[]
  following: string[]

  constructor(data: {
    id: string
    image: string
    username: string
    email: string
    preferences: string[]
    restrictions: string[]
    followers: string[]
    following: string[]
  }) {
    this.id = data.id
    this.image = data.image
    this.username = data.username
    this.email = data.email
    this.preferences = data.preferences
    this.restrictions = data.restrictions
    this.followers = data.followers
    this.following = data.following
  }
}
