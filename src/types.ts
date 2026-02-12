export interface MenuItem {
  id: number
  title: string
  description: string
  price: number
  priceLabel: string
  imageUrl: string
  category: string
}

export interface CartItem extends MenuItem {
  qty: number
}

export type PlateColor = 'red' | 'silver' | 'gold' | 'black' | 'white'

export interface PlateInfo {
  color: PlateColor
  label: string
  labelEn: string
  max: number
}
