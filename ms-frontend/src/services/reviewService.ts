import apiClient from '@/services/axios'
import { Review } from '@/types/Review'
import { LocationReviews } from '@/types/LocationReviews'
import { Location } from '@/types/Location'

export const reviewService = {
  async createReview(text: string, rating: number, location: Location) {
    await apiClient.post('/reviews', {
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
  },
  
  async getReview(reviewId: string) {
    const response = await apiClient.get(`reviews/${reviewId}`)
    return new Review(response.data)
  },

  async getUserReviews(user_id: string): Promise<Review[]> {
    const response = await apiClient.get(`reviews/users/?user_id=${user_id}`)
    return response.data as Review[]
  },
  
  async getReviewByPlaceIds(placeIds: string[]): Promise<LocationReviews[]> {
    const response = await apiClient.request({
      method: 'GET',
      url: `reviews/locations/`,
      data: {
        location_ids: placeIds
      }
    })
    return response.data['location_reviews'].map(
      (locationReviewData: any) => new LocationReviews(locationReviewData)
    )
  }
}
