export class Review {
  review_id: string
  text: string
  rating: number
  image?: File | null
  location: {
    id: string
    name: string
    coordinates: {
      x: string
      y: string
    }
  }

  constructor(data: {
    review_id: string
    text: string
    rating: number
    location: {
      id: string
      name: string
      coordinates: {
        x: string
        y: string 
      } 
    }
    image: File | null
  }) {
    this.review_id = data.review_id
    this.text = data.text
    this.rating = data.rating
    this.location = {
      id: data.location.id, // Corrected from location.id
      name: data.location.name, // Corrected from location.name
      coordinates: {
        x: data.location.coordinates.x, // Corrected from location.coordinates.x
        y: data.location.coordinates.y // Corrected from location.coordinates.y
      }
    };
    this.image = data.image
  }
}
