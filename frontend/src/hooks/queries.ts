import { useQuery } from "@tanstack/vue-query";
import { type Ref, type MaybeRef } from "vue";
import api from "@/api";
import type { DatabaseType } from "@/api";

export function useUsersQuery(
    dbType: Ref<DatabaseType>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["users", dbType],
        queryFn: async () => {
            return api.getUsers(dbType.value);
        },      
        enabled,
    });
}

export function useOrganizationsQuery(
    dbType: Ref<DatabaseType>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["organizations", dbType],
        queryFn: async () => {
            return api.getOrganizations(dbType.value);
        },
        enabled,
    });
}

export function useCampaignsQuery(
    dbType: Ref<DatabaseType>,
    organizationId?: Ref<number | null | undefined>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["campaigns", dbType, organizationId],
        queryFn: async () => {
            const orgId = organizationId?.value;
            return api.getCampaigns(dbType.value, orgId || null);
        },
        enabled,
    });
}

export function useCampaignApplicationsQuery(
    dbType: Ref<DatabaseType>,
    campaignId: Ref<number>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["campaignApplications", dbType, campaignId],
        queryFn: async () => {
            return api.getCampaignApplications(dbType.value, campaignId.value);
        },
        enabled,
    });
}

export function useApplicationsQuery(
    dbType: Ref<DatabaseType>,
    campaignId?: Ref<number | null | undefined>,
    userId?: Ref<number | null | undefined>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["applications", dbType],
        queryFn: async () => {
            return api.getApplications(dbType.value, campaignId?.value || null, userId?.value || null);
        },
        enabled,
    });
}