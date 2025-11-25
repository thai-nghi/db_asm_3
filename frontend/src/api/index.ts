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

// New schemas for account, publication, user_account, and country
export const CountryResponseSchema = z.object({
  id: z.number(),
  code: z.string(),
})

export const AccountResponseSchema = z.object({
  id: z.string(),
  username: z.string(),
  followers: z.number(),
})

export const PublicationResponseSchema = z.object({
  id: z.string(),
  account_id: z.string(),
  type: z.string(),
  insights: z.record(z.string(), z.any()),
})

export const UserAccountResponseSchema = z.object({
  id: z.string(),
  user_id: z.number(),
  account_id: z.string(),
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

// Create schemas for new entities
export const AccountCreateSchema = z.object({
  username: z.string(),
  followers: z.number(),
})

export const PublicationCreateSchema = z.object({
  account_id: z.string(),
  type: z.string(),
  insights: z.record(z.string(), z.any()),
})

export const UserAccountCreateSchema = z.object({
  user_id: z.number(),
  account_id: z.string(),
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

// Update schemas for new entities
export const AccountUpdateSchema = z.object({
  username: z.string().optional(),
  followers: z.number().optional(),
})

export const PublicationUpdateSchema = z.object({
  account_id: z.string().optional(),
  type: z.string().optional(),
  insights: z.record(z.string(), z.any()).optional(),
})

export const UserAccountUpdateSchema = z.object({
  user_id: z.number().optional(),
  account_id: z.string().optional(),
})

// Query parameter schemas
export const CampaignsQueryParamsSchema = z.object({
  organization_id: z.number().optional(),
})

export const ApplicationsQueryParamsSchema = z.object({
  organizer_id: z.number(),
  campaign_id: z.number().optional(),
  user_id: z.number().optional(),
})

// Infer TypeScript types from Zod schemas
export type UserResponse = z.infer<typeof UserResponseSchema>
export type OrganizationResponse = z.infer<typeof OrganizationResponseSchema>
export type CampaignResponse = z.infer<typeof CampaignResponseSchema>
export type CampaignRequirementsResponse = z.infer<typeof CampaignRequirementsResponseSchema>
export type CampaignApplicationResponse = z.infer<typeof CampaignApplicationResponseSchema>
export type CountryResponse = z.infer<typeof CountryResponseSchema>
export type AccountResponse = z.infer<typeof AccountResponseSchema>
export type PublicationResponse = z.infer<typeof PublicationResponseSchema>
export type UserAccountResponse = z.infer<typeof UserAccountResponseSchema>

export type UserCreate = z.infer<typeof UserCreateSchema>
export type OrganizationCreate = z.infer<typeof OrganizationCreateSchema>
export type CampaignCreate = z.infer<typeof CampaignCreateSchema>
export type CampaignRequirementsCreate = z.infer<typeof CampaignRequirementsCreateSchema>
export type CampaignApplicationCreate = z.infer<typeof CampaignApplicationCreateSchema>
export type AccountCreate = z.infer<typeof AccountCreateSchema>
export type PublicationCreate = z.infer<typeof PublicationCreateSchema>
export type UserAccountCreate = z.infer<typeof UserAccountCreateSchema>

export type UserUpdate = z.infer<typeof UserUpdateSchema>
export type OrganizationUpdate = z.infer<typeof OrganizationUpdateSchema>
export type CampaignUpdate = z.infer<typeof CampaignUpdateSchema>
export type CampaignRequirementsUpdate = z.infer<typeof CampaignRequirementsUpdateSchema>
export type CampaignApplicationUpdate = z.infer<typeof CampaignApplicationUpdateSchema>
export type AccountUpdate = z.infer<typeof AccountUpdateSchema>
export type PublicationUpdate = z.infer<typeof PublicationUpdateSchema>
export type UserAccountUpdate = z.infer<typeof UserAccountUpdateSchema>

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

export async function getUsers() {
  const response = await apiRequest<UserResponse[]>('/users')
  return z.array(UserResponseSchema).parse(response)
}

export async function getOrganizations() {
  const response = await apiRequest<OrganizationResponse[]>('/organizations')
  return z.array(OrganizationResponseSchema).parse(response)
}

export async function getCampaigns(organizationId?: number | null) {
  const params = organizationId ? `?organization_id=${organizationId}` : ''
  const response = await apiRequest<CampaignResponse[]>(`/campaigns${params}`)
  return z.array(CampaignResponseSchema).parse(response)
}

export async function getApplications(organizerId?: number | null, campaignId?: number | null, userId?: number | null) {
  const params = new URLSearchParams()
  if (organizerId) params.append('organizer_id', organizerId.toString())
  if (campaignId) params.append('campaign_id', campaignId.toString())
  if (userId) params.append('user_id', userId.toString())
  const queryString = `?${params.toString()}`

  const response = await apiRequest<CampaignApplicationResponse[]>(`/applications${queryString}`)
  return z.array(CampaignApplicationResponseSchema).parse(response)
}

// CREATE ENDPOINTS

export async function createUser(userData: UserCreate) {
  const response = await apiRequest<UserResponse>('/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  })
  return UserResponseSchema.parse(response)
}

export async function createOrganization(organizationData: OrganizationCreate) {
  const response = await apiRequest<OrganizationResponse>('/organizations', {
    method: 'POST',
    body: JSON.stringify(organizationData),
  })
  return OrganizationResponseSchema.parse(response)
}

export async function createCampaign(campaignData: CampaignCreate) {
  const response = await apiRequest<CampaignResponse>('/campaigns', {
    method: 'POST',
    body: JSON.stringify(campaignData),
  })
  return CampaignResponseSchema.parse(response)
}

export async function createApplication(organizerId: number, applicationData: CampaignApplicationCreate) {
  const response = await apiRequest<CampaignApplicationResponse>(`/applications?organizer_id=${organizerId}`, {
    method: 'POST',
    body: JSON.stringify(applicationData),
  })
  return CampaignApplicationResponseSchema.parse(response)
}

// UPDATE ENDPOINTS

export async function updateUser(userId: number, userData: UserUpdate) {
  const response = await apiRequest<UserResponse>(`/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  })
  return UserResponseSchema.parse(response)
}

export async function updateOrganization(organizationId: number, organizationData: OrganizationUpdate) {
  const response = await apiRequest<OrganizationResponse>(`/organizations/${organizationId}`, {
    method: 'PUT',
    body: JSON.stringify(organizationData),
  })
  return OrganizationResponseSchema.parse(response)
}

export async function updateCampaign(campaignId: number, campaignData: CampaignUpdate) {
  const response = await apiRequest<CampaignResponse>(`/campaigns/${campaignId}`, {
    method: 'PUT',
    body: JSON.stringify(campaignData),
  })
  return CampaignResponseSchema.parse(response)
}

export async function updateApplication(organizerId: number, applicationId: number, applicationData: CampaignApplicationUpdate) {
  const response = await apiRequest<CampaignApplicationResponse>(`/applications/${organizerId}/${applicationId}`, {
    method: 'PUT',
    body: JSON.stringify(applicationData),
  })
  return CampaignApplicationResponseSchema.parse(response)
}

// ACCOUNT ENDPOINTS (ScyllaDB only)

export async function createAccount(accountData: AccountCreate) {
  const response = await apiRequest<AccountResponse>('/accounts', {
    method: 'POST',
    body: JSON.stringify(accountData),
  })
  return AccountResponseSchema.parse(response)
}

export async function updateAccount(accountId: string, accountData: AccountUpdate) {
  const response = await apiRequest<AccountResponse>(`/accounts/${accountId}`, {
    method: 'PUT',
    body: JSON.stringify(accountData),
  })
  return AccountResponseSchema.parse(response)
}

// PUBLICATION ENDPOINTS (ScyllaDB only)

export async function getPublications(accountId?: string | null) {
  const params = accountId ? `?account_id=${accountId}` : ''
  const response = await apiRequest<PublicationResponse[]>(`/publications${params}`)
  return z.array(PublicationResponseSchema).parse(response)
}

export async function createPublication(publicationData: PublicationCreate) {
  const response = await apiRequest<PublicationResponse>('/publications', {
    method: 'POST',
    body: JSON.stringify(publicationData),
  })
  return PublicationResponseSchema.parse(response)
}

export async function updatePublication(publicationId: string, publicationData: PublicationUpdate) {
  const response = await apiRequest<PublicationResponse>(`/publications/${publicationId}`, {
    method: 'PUT',
    body: JSON.stringify(publicationData),
  })
  return PublicationResponseSchema.parse(response)
}

// USER ACCOUNT ENDPOINTS (ScyllaDB only)

export async function getUserAccounts(userId: number) {
  const response = await apiRequest<UserAccountResponse[]>(`/users/${userId}/accounts`)
  return z.array(UserAccountResponseSchema).parse(response)
}

export async function createUserAccount(userAccountData: UserAccountCreate) {
  const response = await apiRequest<UserAccountResponse>('/user-accounts', {
    method: 'POST',
    body: JSON.stringify(userAccountData),
  })
  return UserAccountResponseSchema.parse(response)
}

export async function updateUserAccount(userAccountId: string, userAccountData: UserAccountUpdate) {
  const response = await apiRequest<UserAccountResponse>(`/user-accounts/${userAccountId}`, {
    method: 'PUT',
    body: JSON.stringify(userAccountData),
  })
  return UserAccountResponseSchema.parse(response)
}

export async function getUserAccount(userAccountId: string) {
  const response = await apiRequest<UserAccountResponse>(`/user-accounts/${userAccountId}`)
  return UserAccountResponseSchema.parse(response)
}

// USER COUNTRY ENDPOINTS (PostgreSQL only)

export async function getUserCountry(userId: number) {
  const response = await apiRequest<CountryResponse>(`/users/${userId}/country`)
  return CountryResponseSchema.parse(response)
}

export async function setUserCountry(userId: number, countryId: number) {
  const response = await apiRequest<CountryResponse>(`/users/${userId}/country`, {
    method: 'PUT',
    body: JSON.stringify(countryId),
  })
  return CountryResponseSchema.parse(response)
}

export async function getCountries() {
  // Mock data for development
  return [
    { id: 1, code: 'US' },
    { id: 2, code: 'CA' },
    { id: 3, code: 'GB' },
    { id: 4, code: 'FR' },
    { id: 5, code: 'DE' },
    { id: 6, code: 'JP' },
    { id: 7, code: 'CN' },
    { id: 8, code: 'IN' },
    { id: 9, code: 'BR' },
  ]
  // const response = await apiRequest<CountryResponse[]>('/countries')
  // return z.array(CountryResponseSchema).parse(response)
}

// Default export for convenience
const api = {
  // Users
  getUsers,
  createUser,
  updateUser,

  // Organizations
  getOrganizations,
  createOrganization,
  updateOrganization,

  // Campaigns
  getCampaigns,
  createCampaign,
  updateCampaign,

  // Campaign Applications
  getApplications,
  createApplication,
  updateApplication,

  // Accounts
  createAccount,
  updateAccount,

  // Publications
  getPublications,
  createPublication,
  updatePublication,

  // User Accounts
  getUserAccounts,
  createUserAccount,
  updateUserAccount,
  getUserAccount,

  // User Country
  getUserCountry,
  setUserCountry,

  // Countries
  getCountries,
}

export default api