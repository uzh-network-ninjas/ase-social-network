export class Location {
  id: string
  name: string
  type: string

  constructor(data: { id: string; name: string; type: string }) {
    this.id = data.id
    this.name = data.name
    this.type = data.type
  }
}
