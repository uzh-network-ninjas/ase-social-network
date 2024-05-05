import { Location } from '@/types/Location'

export class Review {
  id: string
  userId: string
  username: string
  text: string
  rating: number
  like_count: number
  liked_by_current_user: boolean
  location: Location
  image?: string
  createdAt: Date

  constructor(data: {
    id: string
    user_id: string
    username: string
    text: string
    like_count: number
    liked_by_current_user: boolean
    rating: number
    location: {
      id: string
      name: string
      type: string
      coordinates: {
        x: string
        y: string
      }
    }
    image?: string
    created_at: string
  }) {
    this.id = data.id
    this.userId = data.user_id
    this.username = data.username
    this.text = data.text
    this.like_count = data.like_count
    this.liked_by_current_user = data.liked_by_current_user
    this.rating = data.rating
    this.location = new Location(data.location)
    this.image = data.image
    this.createdAt = new Date(Date.parse(data.created_at))
  }
}
