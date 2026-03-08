import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./CartPage.css";

export const CartPage: React.FC = () => {
    const navigate = useNavigate();
    const [transactions, setTransactions] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTransactions = async () => {
            const token = localStorage.getItem("accessToken");
            if (!token) {
                setLoading(false);
                return;
            }

            try {
                const res = await fetch("http://localhost:8000/transaction/find_all_mine/", {
                    headers: { "Authorization": `Bearer ${token}` }
                });

                if (!res.ok) {
                    throw new Error(`Server error: ${res.status}`);
                }

                const data = await res.json();

                const pending = data.filter((t: any) => !t.is_finished);
                setTransactions(pending);
            } catch (err) {
                console.error("Error fetching transactions:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchTransactions();
    }, []);

    const handleCheckout = async () => {
        const token = localStorage.getItem("accessToken");

        if (!token) {
            alert("Log in to proceed payment");
            navigate("/login");
            return;
        }

        if (transactions.length === 0) return;

        try {
            const res = await fetch("http://localhost:8000/transaction/find_all_mine/", {
                headers: { "Authorization": `Bearer ${token}` }
            });

            if (!res.ok) throw new Error("Cannot fetch transactions");
            const allTransactions = await res.json();

            const pendingTransactions = allTransactions.filter((t: any) => !t.is_finished);

            if (pendingTransactions.length === 0) {
                alert("No pending transactions to finalize.");
                return;
            }

            const promises = pendingTransactions.map(async (transaction: any) => {
                const updateRes = await fetch(
                    `http://localhost:8000/transaction/update/${transaction.transaction_id}/`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`,
                        },
                    }
                );

                if (!updateRes.ok) {
                    const errorText = await updateRes.text();
                    console.error(`Transaction error ${transaction.transaction_id}:`, errorText);
                    throw new Error(`Update error for transaction ${transaction.transaction_id}`);
                }
            });

            await Promise.all(promises);

            alert("Purchase completed successfully! All transactions have been finalized.");

            setTransactions([]);
            localStorage.removeItem("cart");
            navigate("/product/find_all");

        } catch (err) {
            console.error("Checkout error:", err);
            alert("An error occurred while finalizing the payment. Check console for details.");
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate("/login");
    };

    const totalPrice = transactions.reduce((sum, t) => sum + Number(t.total_price), 0);

    if (loading) return <div className="loader">Loading transactions...</div>;

    return (
        <div className="cart-wrapper">
            <header className="top-navbar">
                <div className="logo" onClick={() => navigate("/")}>PixelStore</div>
                <div className="nav-actions">
                    <button className="logout-button" onClick={() => navigate("/product/find_all")}>Store</button>
                    <button className="logout-button" onClick={handleLogout}>Logout</button>
                </div>
            </header>

            <main className="cart-content">
                <h1>Your Shopping Cart</h1>

                {transactions.length === 0 ? (
                    <div className="empty-cart">
                        <p>Your cart is empty.</p>
                        <button className="add-to-cart-btn" onClick={() => navigate("/product/find_all")}>
                            Back to store
                        </button>
                    </div>
                ) : (
                    <div className="cart-layout">
                        <div className="cart-items-list">
                            {transactions.map((t) => (
                                <div key={t.transaction_id} className="cart-item-card">
                                    <div className="cart-item-info">
                                        <h3>Transaction #{t.transaction_id}</h3>
                                        <p>Date: {new Date(t.date_time).toLocaleString()}</p>
                                    </div>
                                    <div className="cart-item-total">
                                        {Number(t.total_price).toFixed(2)} PLN
                                    </div>
                                </div>
                            ))}
                        </div>

                        <aside className="cart-summary">
                            <div className="summary-box">
                                <h3>Summary</h3>
                                <div className="summary-row total">
                                    <span>Total price:</span>
                                    <span>{totalPrice.toFixed(2)} PLN</span>
                                </div>
                                <button className="checkout-button" onClick={handleCheckout}>
                                    Pay Now
                                </button>
                            </div>
                        </aside>
                    </div>
                )}
            </main>
        </div>
    );
};