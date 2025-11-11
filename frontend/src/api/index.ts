import { z } from 'zod'
// Enums
export const MediaTypeSchema = z.enum(['photo', 'video'])
export const ApplicationStatusSchema = z.enum(['pending', 'accept', 'declined'])
export const DatabaseTypeSchema = z.enum(['scylla', 'postgres', 'duckdb'])

export const CampaignRequirements = z.object({
  media_type: MediaTypeSchema,
  count: z.number(),
})

// Response schemas based on backend schemas.py
export const UserResponseSchema = z.object({
  id: z.number(),
  username: z.string(),
  email: z.string(),
})

export const OrganizationResponseSchema = z.object({
  id: z.number(),
  name: z.string(),
})

export const CampaignResponseSchema = z.object({
  id: z.number(),
  organizer_id: z.number(),
  name: z.string(),
  requirements: z.array(CampaignRequirements),
})

export const CampaignRequirementsResponseSchema = z.object({
  id: z.number(),
  campaign_id: z.number(),
  media_type: MediaTypeSchema,
})

export const CampaignApplicationResponseSchema = z.object({
  id: z.number(),
  campaign_id: z.number(),
  user_id: z.number(),
  status: ApplicationStatusSchema,
})

// Create schemas
export const UserCreateSchema = z.object({
  username: z.string(),
  email: z.string(),
  password: z.string(),
})

export const OrganizationCreateSchema = z.object({
  name: z.string(),
})

export const CampaignCreateSchema = z.object({
  organizer_id: z.number(),
  name: z.string(),
  requirements: z.array(CampaignRequirements),
})

export const CampaignRequirementsCreateSchema = z.object({
  campaign_id: z.number(),
  media_type: MediaTypeSchema,
})

export const CampaignApplicationCreateSchema = z.object({
  campaign_id: z.number(),
  user_id: z.number(),
  status: ApplicationStatusSchema,
})

// Update schemas (with optional fields)
export const UserUpdateSchema = z.object({
  username: z.string().optional(),
  email: z.string().optional(),
  password: z.string().optional(),
})

export const OrganizationUpdateSchema = z.object({
  name: z.string().optional(),
})

export const CampaignUpdateSchema = z.object({
  organizer_id: z.number().optional(),
  name: z.string().optional(),
  requirements: z.array(CampaignRequirements).optional(),
})

export const CampaignRequirementsUpdateSchema = z.object({
  campaign_id: z.number().optional(),
  media_type: MediaTypeSchema.optional(),
})

export const CampaignApplicationUpdateSchema = z.object({
  campaign_id: z.number().optional(),
  user_id: z.number().optional(),
  status: ApplicationStatusSchema.optional(),
})

// Query parameter schemas
export const CampaignsQueryParamsSchema = z.object({
  organization_id: z.number().optional(),
})

export const ApplicationsQueryParamsSchema = z.object({
  campaign_id: z.number(),
})

// Infer TypeScript types from Zod schemas
export type UserResponse = z.infer<typeof UserResponseSchema>
export type OrganizationResponse = z.infer<typeof OrganizationResponseSchema>
export type CampaignResponse = z.infer<typeof CampaignResponseSchema>
export type CampaignRequirementsResponse = z.infer<typeof CampaignRequirementsResponseSchema>
export type CampaignApplicationResponse = z.infer<typeof CampaignApplicationResponseSchema>

export type UserCreate = z.infer<typeof UserCreateSchema>
export type OrganizationCreate = z.infer<typeof OrganizationCreateSchema>
export type CampaignCreate = z.infer<typeof CampaignCreateSchema>
export type CampaignRequirementsCreate = z.infer<typeof CampaignRequirementsCreateSchema>
export type CampaignApplicationCreate = z.infer<typeof CampaignApplicationCreateSchema>

export type UserUpdate = z.infer<typeof UserUpdateSchema>
export type OrganizationUpdate = z.infer<typeof OrganizationUpdateSchema>
export type CampaignUpdate = z.infer<typeof CampaignUpdateSchema>
export type CampaignRequirementsUpdate = z.infer<typeof CampaignRequirementsUpdateSchema>
export type CampaignApplicationUpdate = z.infer<typeof CampaignApplicationUpdateSchema>

export type MediaType = z.infer<typeof MediaTypeSchema>
export type ApplicationStatus = z.infer<typeof ApplicationStatusSchema>
export type DatabaseType = z.infer<typeof DatabaseTypeSchema>
export type CampaignsQueryParams = z.infer<typeof CampaignsQueryParamsSchema>
export type ApplicationsQueryParams = z.infer<typeof ApplicationsQueryParamsSchema>

// API Configuration
const API_BASE_URL = 'http://localhost:8000' // Adjust based on your backend URL

// Helper function for API calls
async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`)
  }

  return response.json()
}

// READ ENDPOINTS

export async function getUsers(dbType: DatabaseType) {
  const response = await apiRequest<UserResponse[]>(`/${dbType}/users`)
  return z.array(UserResponseSchema).parse(response)
}

export async function getOrganizations(dbType: DatabaseType) {
  const response = await apiRequest<OrganizationResponse[]>(`/${dbType}/organizations`)
  return z.array(OrganizationResponseSchema).parse(response)
}

export async function getCampaigns(dbType: DatabaseType, organizationId?: number | null) {
  const params = organizationId ? `?organization_id=${organizationId}` : ''
  const response = await apiRequest<CampaignResponse[]>(`/${dbType}/campaigns${params}`)
  return z.array(CampaignResponseSchema).parse(response)
}

export async function getCampaignApplications(dbType: DatabaseType, campaignId: number) {
  const response = await apiRequest<CampaignApplicationResponse[]>(`/${dbType}/campaigns/${campaignId}/applications`)
  return z.array(CampaignApplicationResponseSchema).parse(response)
}

export async function getApplications(dbType: DatabaseType, campaignId?: number | null, userId?: number | null) {
  const params = new URLSearchParams()
  if (campaignId) params.append('campaign_id', campaignId.toString())
  if (userId) params.append('user_id', userId.toString())
  const queryString = params.toString() ? `?${params.toString()}` : ''
  
  const response = await apiRequest<CampaignApplicationResponse[]>(`/${dbType}/applications${queryString}`)
  return z.array(CampaignApplicationResponseSchema).parse(response)
}

// CREATE ENDPOINTS

export async function createUser(dbType: DatabaseType, userData: UserCreate) {
  const response = await apiRequest<UserResponse>(`/${dbType}/users`, {
    method: 'POST',
    body: JSON.stringify(userData),
  })
  return UserResponseSchema.parse(response)
}

export async function createOrganization(dbType: DatabaseType, organizationData: OrganizationCreate) {
  const response = await apiRequest<OrganizationResponse>(`/${dbType}/organizations`, {
    method: 'POST',
    body: JSON.stringify(organizationData),
  })
  return OrganizationResponseSchema.parse(response)
}

export async function createCampaign(dbType: DatabaseType, campaignData: CampaignCreate) {
  const response = await apiRequest<CampaignResponse>(`/${dbType}/campaigns`, {
    method: 'POST',
    body: JSON.stringify(campaignData),
  })
  return CampaignResponseSchema.parse(response)
}

export async function createApplication(dbType: DatabaseType, applicationData: CampaignApplicationCreate) {
  const response = await apiRequest<CampaignApplicationResponse>(`/${dbType}/applications`, {
    method: 'POST',
    body: JSON.stringify(applicationData),
  })
  return CampaignApplicationResponseSchema.parse(response)
}

// UPDATE ENDPOINTS

export async function updateUser(dbType: DatabaseType, userId: number, userData: UserUpdate) {
  const response = await apiRequest<UserResponse>(`/${dbType}/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  })
  return UserResponseSchema.parse(response)
}

export async function updateOrganization(dbType: DatabaseType, organizationId: number, organizationData: OrganizationUpdate) {
  const response = await apiRequest<OrganizationResponse>(`/${dbType}/organizations/${organizationId}`, {
    method: 'PUT',
    body: JSON.stringify(organizationData),
  })
  return OrganizationResponseSchema.parse(response)
}

export async function updateCampaign(dbType: DatabaseType, campaignId: number, campaignData: CampaignUpdate) {
  const response = await apiRequest<CampaignResponse>(`/${dbType}/campaigns/${campaignId}`, {
    method: 'PUT',
    body: JSON.stringify(campaignData),
  })
  return CampaignResponseSchema.parse(response)
}

export async function updateApplication(dbType: DatabaseType, applicationId: number, applicationData: CampaignApplicationUpdate) {
  const response = await apiRequest<CampaignApplicationResponse>(`/${dbType}/applications/${applicationId}`, {
    method: 'PUT',
    body: JSON.stringify(applicationData),
  })
  return CampaignApplicationResponseSchema.parse(response)
}

// Default export for convenience
const api = {
  // READ ENDPOINTS
  getUsers,
  getOrganizations,
  getCampaigns,
  getCampaignApplications,
  getApplications,
  
  // CREATE ENDPOINTS
  createUser,
  createOrganization,
  createCampaign,
  createApplication,
  
  // UPDATE ENDPOINTS
  updateUser,
  updateOrganization,
  updateCampaign,
  updateApplication,

}

export default api