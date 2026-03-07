import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { findByUsername } from "../../api/user";
import type { UserData } from "../../types/user";
import "./SelfUserProfilePage.css";

export const SelfUserProfilePage: React.FC = () => {
    const { username } = useParams<{ username: string }>();
    const navigate = useNavigate();

    const [user, setUser] = useState<UserData | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem("accessToken");

            if (!token || !username) {
                setError("Missing authentication or username.");
                setLoading(false);
                return;
            }

            try {
                const data = await findByUsername(username, token);
                setUser(data);
            } catch (err) {
                setError("Could not load user profile.");
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [username]);

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        navigate("/login");
    };

    if (loading) return <div className="loader">Loading profile...</div>;
    if (error) return <div className="error-profile">{error}</div>;

    return (
    <div className="profile-container">
        <div className="profile-content">
            <div className="profile-box">
                <h1>User Profile</h1>

                <div className="user-info">
                    <p><strong>Username:</strong> {user?.username}</p>
                    <p><strong>Bio:</strong> {user?.bio || "No bio available"}</p>
                    <p><strong>Balance:</strong> <span className="money-amount">${user?.money}</span></p>
                </div>

                <div className="button-grid">
                    <button
                        onClick={() => navigate(`/user_preferences/find_by_username/${username}`)}
                        className="btn-secondary"
                    >
                        User Preferences
                    </button>
                    <button
                        onClick={() => navigate(`/user_statistics/find_by_username/${username}`)}
                        className="btn-secondary"
                    >
                        User Statistics
                    </button>
                    <button
                        onClick={() => navigate("/product/find_all")}
                        className="btn-primary"
                    >
                        Go Shopping
                    </button>
                    <button onClick={handleLogout} className="btn-logout">
                        Logout
                    </button>
                </div>
            </div>
        </div>
    </div>
    );
};