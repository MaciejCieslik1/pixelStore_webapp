import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../api/authentication";
import type { RegisterData } from "../../types/authentication";
import "./RegisterPage.css";

export const RegisterPage: React.FC = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState<RegisterData>({
        username: "",
        email: "",
        password: "",
        address: "",
        postal_code: "",
        city: "",
        country: "",
    });

    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (field: keyof RegisterData, value: string) => {
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
            const res = await register(form);
            setMessage(res.msg || "Account created successfully!");
            setForm({
                username: "",
                email: "",
                password: "",
                address: "",
                postal_code: "",
                city: "",
                country: "",
            });
        } catch (err: any) {
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
                <h1>Registration</h1>

                {message && <div className="success">{message}</div>}
                {error && <div className="error">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <label>Username</label>
                    <input
                        type="text"
                        value={form.username}
                        onChange={(e) => handleChange("username", e.target.value)}
                        placeholder="Enter username"
                        disabled={loading}
                    />

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
                        onChange={(e) => handleChange("password", e.target.value)}
                        placeholder="Enter password"
                        disabled={loading}
                    />

                    <label>Address</label>
                    <input
                        type="text"
                        value={form.address}
                        onChange={(e) => handleChange("address", e.target.value)}
                        placeholder="Enter Street and house number"
                        disabled={loading}
                    />

                    <div className="form-row">
                        <div className="form-group">
                            <label>Postal Code</label>
                            <input
                                type="text"
                                value={form.postal_code}
                                onChange={(e) => handleChange("postal_code", e.target.value)}
                                placeholder="Enter postal code"
                                disabled={loading}
                            />
                        </div>
                        <div className="form-group">
                            <label>City</label>
                            <input
                                type="text"
                                value={form.city}
                                onChange={(e) => handleChange("city", e.target.value)}
                                placeholder="Enter city"
                                disabled={loading}
                            />
                        </div>
                    </div>

                    <label>Country</label>
                    <input
                        type="text"
                        value={form.country}
                        onChange={(e) => handleChange("country", e.target.value)}
                        placeholder="Enter country"
                        disabled={loading}
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Registering..." : "Register"}
                    </button>

                    <p className="verify-prompt">
                        Already have a code?{" "}
                        <button
                            type="button"
                            className="link-button"
                            onClick={() => navigate("/verify_account")}
                        >
                            Verify account
                        </button>
                    </p>
                </form>
            </div>
        </div>
    );
};
