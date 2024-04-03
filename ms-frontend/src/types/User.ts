export class User {
  id: string
  username: string
  email: string
  preferences?: string[]
  //added
  
  followers?: List<User>
  following?: List<User>
  reviews?: number
  image?: string

  constructor(data: { id: string; username: string; email: string; preferences?: string[]; followers?: List<User>; following?: List<User>; reviews?: number; image?: string}) {
    this.id = data.id
    this.username = data.username
    this.email = data.email
    this.preferences = data.preferences
    // added
    this.followers = data.followers
    this.following = data.following
    this.reviews = data.reviews
    this.image = data.image

  }
}
