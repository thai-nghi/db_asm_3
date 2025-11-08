import { useQuery } from "@tanstack/vue-query";
import { Ref, MaybeRef } from "vue";
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
    organizationId?: Ref<number | undefined>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["campaigns", dbType, organizationId],
        queryFn: async () => {
            return api.getCampaigns(dbType.value, organizationId?.value);
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