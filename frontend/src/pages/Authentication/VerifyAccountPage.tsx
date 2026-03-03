import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyAccount} from "../../api/authentication";
import "./RegisterPage.css";
import type {VerifyAccountData} from "../../types/authentication.ts";

export const VerifyAccountPage: React.FC = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState<VerifyAccountData>({
        email: "",
        verification_code: "",
    });

    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (field: keyof VerifyAccountData, value: string) => {
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
            const res = await verifyAccount(form);
            setMessage(res.msg || "Account verified successfully!");
            setForm({
                email: "",
                verification_code: "",
            });
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
                <h1>Verification</h1>

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

                    <label>Verification code</label>
                    <input
                        type="text"
                        value={form.verification_code}
                        onChange={(e) => handleChange("verification_code",
                            e.target.value)}
                        placeholder="Enter verification code from your mailbox"
                        disabled={loading}
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Verifying..." : "Verify"}
                    </button>

                    <p className="verify-prompt">
                        Already verified?{" "}
                        <button
                            type="button"
                            className="link-button"
                            onClick={() => navigate("/login")}
                        >
                            Login
                        </button>
                    </p>
                </form>
            </div>
        </div>
    );
};
