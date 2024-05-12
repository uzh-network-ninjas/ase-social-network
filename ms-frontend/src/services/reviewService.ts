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
  async getReviews(timestamp_cursor?: Date): Promise<Review[]> {
    const response = await apiClient.get(`reviews/`, {
      params: {
        timestamp_cursor: timestamp_cursor ? formatDateTime(timestamp_cursor) : undefined
      }
    })
    return response.data.reviews.map((review: any) => new Review(review))
  },

  async getUserReviews(user_id: string): Promise<Review[]> {
    const response = await apiClient.get('reviews/users/', { params: { user_id: user_id } })
    return response.data.reviews.map((review: any) => new Review(review))
  },

  async getReviewByPlaceIds(placeIds: string[]): Promise<LocationReviews[]> {
    const paramString = placeIds.map((item) => `location_id=${item}`).join('&')
    const response = await apiClient.request({
      method: 'GET',
      url: `reviews/locations/?${paramString}`
    })
    return response.data['location_reviews'].map(
      (locationReviewData: any) => new LocationReviews(locationReviewData)
    )
  },

  async likeReview(review_id: string) {
    await apiClient.patch(`reviews/${review_id}/likes`)
  },

  async unlikeReview(review_id: string) {
    await apiClient.delete(`reviews/${review_id}/likes`)
  }
}

function formatDateTime(date: Date) {
  // Helper function to pad numbers to two digits
  function pad(number: number, length: number) {
    return number.toString().padStart(length, '0')
  }

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1, 2)
  const day = pad(date.getDate(), 2)
  const hour = pad(date.getHours(), 2)
  const minute = pad(date.getMinutes(), 2)
  const second = pad(date.getSeconds(), 2)
  const millisecond = pad(date.getMilliseconds(), 6) // Extend to 6 digits

  return `${year}-${month}-${day}T${hour}:${minute}:${second}.${millisecond}`
}
