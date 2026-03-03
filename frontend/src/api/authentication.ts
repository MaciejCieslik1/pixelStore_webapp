import { apiFetch } from "./client";
import type {RegisterData, LoginData, Tokens, ResetPasswordData, VerifyAccountData} from "../types/authentication.ts";

export const register = async (data: RegisterData) => {
    try {
        const response = await apiFetch<{ msg?: string; error?: string }>(
            "/register/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data)
            }
        );

        if (response.error) {
            throw response;
        }

        return response;
    }
    catch (err) {
        throw err;
    }
};

export const login = (data: LoginData) => {
  return apiFetch<Tokens>("/login/", { method: "POST", body: data });
};


export const logout = (access_token: string) => {
  return apiFetch<{ msg: string }>("/logout/", {
    method: "POST",
    headers: { Authorization: `Bearer ${access_token}` },
  });
};


export const verifyAccount = async (data: VerifyAccountData) => {
    try {
        const response = await apiFetch<{ msg?: string; error?: string }>(
            "/verify_account/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data)
            }
        );

        if (response.error) throw response;
        return response;
    }
    catch (err) {
        throw err;
    }
};


export const verifyToken = (token: string) => {
  return apiFetch<{ valid: boolean; msg?: string; error?: string }>("/verify_token/", {
    method: "POST",
    body: { token },
  });
};


export const refreshToken = (refresh_token: string) => {
  return apiFetch<{ access_token: string }>("/refresh_token/", {
    method: "POST",
    body: { token: refresh_token },
  });
};


export const resetPassword = (data: ResetPasswordData, access_token: string) => {
  return apiFetch<{ msg: string }>("/reset_password/", {
    method: "POST",
    body: data,
    headers: { Authorization: `Bearer ${access_token}` },
  });
};


export const resendVerificationCode = (access_token: string) => {
  return apiFetch<{ msg: string }>("/resend_verification_code/", {
    method: "POST",
    headers: { Authorization: `Bearer ${access_token}` },
  });
};
