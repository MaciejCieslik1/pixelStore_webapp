import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../api/authentication";
import "./RegisterPage.css";
import type {LoginData} from "../../types/authentication.ts";

export const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState<LoginData>({
        email: "",
        password: "",
    });

    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (field: keyof LoginData, value: string) => {
        setForm({ ...form, [field]: value });
    };

    const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        const isFormIncomplete = Object.values(form).some(value => !value.trim());
        if (isFormIncomplete) {
            setError("All fields are required!");
            return;
        }

        try {
            setLoading(true);
            const res = await login(form);

            localStorage.setItem("accessToken", res.access_token);
            localStorage.setItem("refreshToken", res.refresh_token);

            setMessage("Logged successfully!");

            setTimeout(() => {
                navigate("/product/find_all");
            }, 500);
        }
        catch (err: any) {
            if (err && typeof err === "object") {
                const firstErrorMessage = Object.values(err)[0];
                setError(typeof firstErrorMessage === "string" ? firstErrorMessage : "Validation error");
            } else {
                setError("Something went wrong. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-box">
                <h1>Log in</h1>

                {message && <div className="success">{message}</div>}
                {error && <div className="error">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <label>Email</label>
                    <input
                        type="email"
                        value={form.email}
                        onChange={(e) => handleChange("email", e.target.value)}
                        placeholder="Enter email"
                        disabled={loading}
                    />

                    <label>Password</label>
                    <input
                        type="password"
                        value={form.password}
                        onChange={(e) => handleChange("password",
                            e.target.value)}
                        placeholder="Enter password"
                        disabled={loading}
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Logging..." : "Login"}
                    </button>

                    <p className="verify-prompt">
                        Don't have account?{" "}
                        <button
                            type="button"
                            className="link-button"
                            onClick={() => navigate("/register")}
                        >
                            Register
                        </button>
                    </p>
                </form>
            </div>
        </div>
    );
};

