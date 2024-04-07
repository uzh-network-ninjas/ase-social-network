export class Review {
  review_id: string
  text: string
  rating: number
  locationId: string
  image?: string

  constructor(data: {
    review_id: string
    text: string
    rating: number
    locationId: string
    image?: string
  }) {
    this.review_id = data.review_id
    this.text = data.text
    this.rating = data.rating
    this.locationId = data.locationId
    this.image = data.image
  }
}
