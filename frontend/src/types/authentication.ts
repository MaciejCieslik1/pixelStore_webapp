export interface RegisterData {
  username: string;
  email: string;
  password: string;
  address: string;
  postal_code: string;
  city: string;
  country: string;
}

export interface VerifyAccountData {
  email: string;
  verification_code: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
}

export interface VerifyTokenData {
  token: string;
}

export interface ResetPasswordData {
  new_password: string;
  confirm_password: string;
  verification_code: string;
}
