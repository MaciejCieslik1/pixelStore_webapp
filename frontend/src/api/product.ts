import type {ProductDetailsData} from "../types/product";
import {apiFetch} from "./client.ts";

export interface ProductFilters {
    searchTerm?: string;
    sortBy?: string;
    order?: string;
    minPrice?: string;
    maxPrice?: string;
    status?: string;
}

export const findAll = (filters: ProductFilters, token: string) => {
    const params = new URLSearchParams();
    if (filters.searchTerm) params.append("search", filters.searchTerm);
    if (filters.sortBy) params.append("sort_by", filters.sortBy);
    if (filters.order) params.append("order", filters.order);
    if (filters.minPrice) params.append("min_price", filters.minPrice);
    if (filters.maxPrice) params.append("max_price", filters.maxPrice);
    if (filters.status) params.append("status", filters.status);

    return apiFetch<ProductDetailsData[]>(`/product/find_all/?${params.toString()}`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
    });
};

export const findById = (productId: string, token: string) => {
    return apiFetch<ProductDetailsData>(`/product/find_by_id/${productId}/`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
    });
};