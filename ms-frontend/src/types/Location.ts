export class Location {
  id: string
  name: string
  type: string
  coordinates: {
    x: string
    y: string
  }

  constructor(data: {
    id: string
    name: string
    type: string
    coordinates: { x: string; y: string }
  }) {
    this.id = data.id
    this.name = data.name
    this.type = data.type
    this.coordinates = {
      x: data.coordinates.x,
      y: data.coordinates.y
    }
  }
}
