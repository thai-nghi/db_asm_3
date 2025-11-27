// Shared type definitions for the application
// Based on backend schemas.py

export type User = {
  id: number
  username: string
  email: string
}

export type Organization = {
  id: number
  name: string
}

export type MediaType = 'photo' | 'video'

export type Requirements = {
  media_type: MediaType
  count: number
}

export type CampaignData = {
  id: number
  organizer_id: number
  name: string
  requirements: Requirements[]
}

export type CampaignCreateData = {
  organizer_id: number
  name: string
  requirements: Requirements[]
}

export type Application = {
  id: number
  campaign_id: number
  user_id: number
  status: 'PENDING' | 'APPROVED' | 'REJECTED'
}

export type Account = {
  id: string
  username: string
  followers: number
}

export type PublicationInsights = {
  likes: number
  comments: number
}

export type Publication = {
  id: string
  account_id: string
  type: string
  insights: PublicationInsights
}

// Database types
export type DatabaseType = 'postgres' | 'duckdb' | 'scylla'

// Table column configuration for BaseTable component
export type TableColumn = {
  key: string
  label: string
  type?: 'text' | 'badge' | 'accent' | 'default'
  badgeClass?: string
  accentClass?: string
}

// Event handlers type definitions
export type TableEvents<T> = {
  add: () => void
  edit: (item: T) => void
  delete: (item: T) => void
}