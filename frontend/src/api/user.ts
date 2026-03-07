import {apiFetch} from "./client.ts";
import type {UserData} from "../types/user.ts";

export const findByUsername = (username: string, token: string) => {
    return apiFetch<UserData>(`/user/find_by_username/${username}/`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
    });
};