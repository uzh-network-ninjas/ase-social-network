import { Review } from '@/types/Review'

export class LocationReviews {
  locationId: string
  averageRating: number
  reviews: Review[]

  constructor(data: { location_id: string; average_rating: number; reviews: any[] }) {
    this.locationId = data.location_id
    this.averageRating = data.average_rating
    this.reviews = data.reviews.map((review: any) => new Review(review))
  }
}
