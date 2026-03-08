import {jwtDecode} from "jwt-decode";
import type {TokenPayload} from "../types/authentication.ts";

export const getUsernameFromToken = (): string | null => {
    const token = localStorage.getItem("accessToken");
    if (!token) return null;

    try {
        const decoded = jwtDecode<TokenPayload>(token);
        return decoded.username;
    } catch (err) {
        return null;
    }
};