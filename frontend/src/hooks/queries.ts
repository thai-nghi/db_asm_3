import { useQuery } from "@tanstack/vue-query";
import { type Ref, type MaybeRef } from "vue";
import api from "@/api";

export function useUsersQuery(
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["users"],
        queryFn: async () => {
            return api.getUsers();
        },
        enabled,
    });
}

export function useOrganizationsQuery(
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["organizations"],
        queryFn: async () => {
            return api.getOrganizations();
        },
        enabled,
    });
}

export function useCampaignsQuery(
    organizationId?: Ref<number | null | undefined>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["campaigns", organizationId],
        queryFn: async () => {
            const orgId = organizationId?.value;
            return api.getCampaigns(orgId || null);
        },
        enabled,
    });
}

export function useApplicationsQuery(
    organizerId?: Ref<number | null | undefined>,
    campaignId?: Ref<number | null | undefined>,
    userId?: Ref<number | null | undefined>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["applications", campaignId, userId],
        queryFn: async () => {
            return api.getApplications(organizerId?.value, campaignId?.value || null, userId?.value || null);
        },
        enabled,
    });
}

// ACCOUNT QUERIES (ScyllaDB only)

export function usePublicationsQuery(
    accountId?: Ref<string | null | undefined>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["publications", accountId],
        queryFn: async () => {
            return api.getPublications(accountId?.value || null);
        },
        enabled,
    });
}

// USER ACCOUNT QUERIES (ScyllaDB only)

export function useUserAccountsQuery(
    userId: Ref<number>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["userAccounts", userId],
        queryFn: async () => {
            return api.getUserAccounts(userId.value);
        },
        enabled,
    });
}

export function useUserAccountQuery(
    userAccountId: Ref<string>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["userAccount", userAccountId],
        queryFn: async () => {
            try {
                const result = await api.getUserAccount(userAccountId.value);
                // Return null if we get an empty state (empty id)
                return result.id === "" ? null : result;
            } catch (error) {
                // Handle any potential errors gracefully
                return null;
            }
        },
        enabled,
    });
}

// USER COUNTRY QUERIES (PostgreSQL only)

export function useUserCountryQuery(
    userId: Ref<number>,
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["userCountry", userId],
        queryFn: async () => {
            try {
                const result = await api.getUserCountry(userId.value);
                // Return null if we get an empty state (id === 0)
                return result.id === 0 ? null : result;
            } catch (error) {
                // Handle any potential errors gracefully
                return null;
            }
        },
        enabled,
    });
}

export function useCountriesQuery(
    enabled: MaybeRef<boolean> = true
) {
    return useQuery({
        queryKey: ["countries"],
        queryFn: async () => {
            return api.getCountries();
        },
        enabled,
    });
}