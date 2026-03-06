import {apiFetch} from "./client.ts";
import type {TransactionData} from "../types/transaction.ts";

export const findAllMine = (token: string) => {
    return apiFetch<TransactionData>(`/transaction/find_all_mine/`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
    });
};