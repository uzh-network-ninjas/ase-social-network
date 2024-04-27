import apiClient from '@/services/axios'
import { Review } from '@/types/Review'
import { LocationReviews } from '@/types/LocationReviews'

export const reviewService = {
  async getReview(reviewId: string) {
    const response = await apiClient.get(`reviews/${reviewId}`)
    return new Review(response.data)
  },

  // async getReviewFeed(timestamp : Date ) : Promise<Review[]> {
  //     const response = await apiClient.get(`reviews/${timestamp}`)
  //     return response.data as Review[];
  // },

  async getUserReviews(username: string): Promise<Review[]> {
    const response = await apiClient.get(`reviews/users/${username}`)
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
