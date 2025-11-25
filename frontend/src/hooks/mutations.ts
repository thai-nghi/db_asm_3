import { useMutation, useQueryClient } from "@tanstack/vue-query";
import type { Ref } from "vue";
import api from "@/api";
import type {
  DatabaseType,
  UserCreate,
  UserUpdate,
  OrganizationCreate,
  OrganizationUpdate,
  CampaignCreate,
  CampaignUpdate,
  CampaignApplicationCreate,
  CampaignApplicationUpdate,
  AccountCreate,
  AccountUpdate,
  PublicationCreate,
  PublicationUpdate,
  UserAccountCreate,
  UserAccountUpdate
} from "@/api";

// CREATE MUTATIONS

export function useCreateUserMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userData: UserCreate) => {
      return api.createUser(userData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

export function useCreateOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (organizationData: OrganizationCreate) => {
      return api.createOrganization(organizationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
    },
  });
}

export function useCreateCampaignMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (campaignData: CampaignCreate) => {
      return api.createCampaign(campaignData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns"] });
    },
  });
}

export function useCreateApplicationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ organizerId, applicationData }: { organizerId: number, applicationData: CampaignApplicationCreate }) => {
      return api.createApplication(organizerId, applicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });
}

// UPDATE MUTATIONS

export function useUpdateUserMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ userId, userData }: { userId: number; userData: UserUpdate }) => {
      return api.updateUser(userId, userData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

export function useUpdateOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ organizationId, organizationData }: { organizationId: number; organizationData: OrganizationUpdate }) => {
      return api.updateOrganization(organizationId, organizationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations"] });
    },
  });
}

export function useUpdateCampaignMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ campaignId, campaignData }: { campaignId: number; campaignData: CampaignUpdate }) => {
      return api.updateCampaign(campaignId, campaignData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns"] });
    },
  });
}

export function useUpdateApplicationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ organizerId, applicationId, applicationData }: { organizerId: number, applicationId: number; applicationData: CampaignApplicationUpdate }) => {
      return api.updateApplication(organizerId, applicationId, applicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });
}

// ACCOUNT MUTATIONS (ScyllaDB only)

export function useCreateAccountMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (accountData: AccountCreate) => {
      return api.createAccount(accountData);
    },
    onSuccess: () => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ["publications"] });
      queryClient.invalidateQueries({ queryKey: ["userAccounts"] });
    },
  });
}

export function useUpdateAccountMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ accountId, accountData }: { accountId: string; accountData: AccountUpdate }) => {
      return api.updateAccount(accountId, accountData);
    },
    onSuccess: () => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ["publications"] });
      queryClient.invalidateQueries({ queryKey: ["userAccounts"] });
    },
  });
}

// PUBLICATION MUTATIONS (ScyllaDB only)

export function useCreatePublicationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (publicationData: PublicationCreate) => {
      return api.createPublication(publicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["publications"] });
    },
  });
}

export function useUpdatePublicationMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ publicationId, publicationData }: { publicationId: string; publicationData: PublicationUpdate }) => {
      return api.updatePublication(publicationId, publicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["publications"] });
    },
  });
}

// USER ACCOUNT MUTATIONS (ScyllaDB only)

export function useCreateUserAccountMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userAccountData: UserAccountCreate) => {
      return api.createUserAccount(userAccountData);
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["userAccounts", variables.user_id] });
    },
  });
}

export function useUpdateUserAccountMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ userAccountId, userAccountData }: { userAccountId: string; userAccountData: UserAccountUpdate }) => {
      return api.updateUserAccount(userAccountId, userAccountData);
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["userAccounts"] });
      queryClient.invalidateQueries({ queryKey: ["userAccount", variables.userAccountId] });
    },
  });
}

// USER COUNTRY MUTATIONS (PostgreSQL only)

export function useSetUserCountryMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ userId, countryId }: { userId: number; countryId: number }) => {
      return api.setUserCountry(userId, countryId);
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["userCountry", variables.userId] });
    },
  });
}
