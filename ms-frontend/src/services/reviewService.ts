import apiClient from '@/services/axios'
import { Review } from '@/types/Review'
import { LocationReviews } from '@/types/LocationReviews'
import { Location } from '@/types/Location'

export const reviewService = {
  async createReview(text: string, rating: number, location: Location) {
    const response = await apiClient.post('/reviews', {
      text: text,
      rating: rating,
      location: {
        id: location.id,
        name: location.name,
        type: location.type,
        coordinates: {
          x: location.coordinates.x,
          y: location.coordinates.y
        }
      }
    })
    return new Review(response.data)
  },
  async appendReviewImage(reviewId: string, file: File) {
    const formData = new FormData()
    formData.append('review_id', reviewId)
    formData.append('image', file)

    const response = await apiClient.patch('reviews/image', formData)
    return new Review(response.data)
  },
  async getReview(reviewId: string) {
    const response = await apiClient.get(`reviews/${reviewId}`)
    return new Review(response.data)
  },

  async getUserReviews(user_id: string): Promise<Review[]> {
    const response = await apiClient.get('reviews/users/', { params: { user_id: user_id } })
    return response.data.reviews.map((review : any) => new Review(review))
  },

  async getReviewByPlaceIds(placeIds: string[]): Promise<LocationReviews[]> {
    const paramString = placeIds.map(item => `location_id=${item}`).join('&')
    const response = await apiClient.request({
      method: 'GET',
      url: `reviews/locations/?${paramString}`,
    })
    return response.data['location_reviews'].map(
      (locationReviewData: any) => new LocationReviews(locationReviewData)
    )
  }
}
