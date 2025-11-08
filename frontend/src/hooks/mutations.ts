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
  CampaignRequirementsCreate,
  CampaignApplicationCreate,
  CampaignApplicationUpdate
} from "@/api";

// CREATE MUTATIONS

export function useCreateUserMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (userData: UserCreate) => {
      return api.createUser(dbType.value, userData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users", dbType] });
    },
  });
}

export function useCreateOrganizationMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (organizationData: OrganizationCreate) => {
      return api.createOrganization(dbType.value, organizationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations", dbType] });
    },
  });
}

export function useCreateCampaignMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (campaignData: CampaignCreate) => {
      return api.createCampaign(dbType.value, campaignData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns", dbType] });
    },
  });
}

export function useCreateCampaignRequirementsMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (requirementsData: CampaignRequirementsCreate) => {
      return api.createCampaignRequirements(dbType.value, requirementsData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaignRequirements", dbType] });
    },
  });
}

export function useCreateApplicationMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (applicationData: CampaignApplicationCreate) => {
      return api.createApplication(dbType.value, applicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaignApplications", dbType] });
    },
  });
}

// UPDATE MUTATIONS

export function useUpdateUserMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ userId, userData }: { userId: number; userData: UserUpdate }) => {
      return api.updateUser(dbType.value, userId, userData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users", dbType] });
    },
  });
}

export function useUpdateOrganizationMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ organizationId, organizationData }: { organizationId: number; organizationData: OrganizationUpdate }) => {
      return api.updateOrganization(dbType.value, organizationId, organizationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["organizations", dbType] });
    },
  });
}

export function useUpdateCampaignMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ campaignId, campaignData }: { campaignId: number; campaignData: CampaignUpdate }) => {
      return api.updateCampaign(dbType.value, campaignId, campaignData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaigns", dbType] });
    },
  });
}

export function useUpdateApplicationMutation(dbType: Ref<DatabaseType>) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ applicationId, applicationData }: { applicationId: number; applicationData: CampaignApplicationUpdate }) => {
      return api.updateApplication(dbType.value, applicationId, applicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["campaignApplications", dbType] });
    },
  });
}
