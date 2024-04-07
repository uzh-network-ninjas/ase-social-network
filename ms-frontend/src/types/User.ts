import { Review } from '@/types/Review'

export class User {
  id: string
  username: string
  email: string
  preferences?: string[]
  //added

  followers: List<User>
  following: List<User>
  image?: File

  constructor(data: {
    id: string
    username: string
    email: string
    preferences?: string[]
    followers: List<User>
    following: List<User>
    image?: File
  }) {
    this.id = data.id
    this.username = data.username
    this.email = data.email
    this.preferences = data.preferences
    // added
    this.followers = data.followers
    this.following = data.following
    this.image = data.image
  }
}
