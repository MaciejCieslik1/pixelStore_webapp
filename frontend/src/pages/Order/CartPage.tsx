import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import type { ProductDetailsData } from "../../types/product.ts";
import "./CartPage.css";

interface CartItem extends ProductDetailsData {
    quantity: number;
}

export const CartPage: React.FC = () => {
    const navigate = useNavigate();
    const [cartItems, setCartItems] = useState<CartItem[]>([]);

    useEffect(() => {
        const savedCart = localStorage.getItem("cart");
        if (savedCart) {
            setCartItems(JSON.parse(savedCart));
        }
    }, []);

    const removeItem = (id: number) => {
        const updated = cartItems.filter(item => item.product_id !== id);
        setCartItems(updated);
        localStorage.setItem("cart", JSON.stringify(updated));
    };

    const totalPrice = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    const handleCheckout = async () => {
        const token = localStorage.getItem("accessToken");

        if (!token) {
            alert("Log in to proceed payment");
            navigate("/login");
            return;
        }

        if (cartItems.length === 0) return;

        try {

            const res = await fetch("http://localhost:8000/transaction/find_all_mine", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
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
                    `http://localhost:8000/transaction/update/${transaction.transaction_id}`,
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`,
                        }
                    }
                );

                if (!updateRes.ok) throw new Error("Update error");
            });

            await Promise.all(promises);

            alert("Purchase completed successfully! All transactions have been finalized.");

            setCartItems([]);
            localStorage.removeItem("cart");
            navigate("/product/find_all");

        } catch (err) {
            console.error("Checkout error:", err);
            alert("An error occurred while finalizing the payment.");
    }
};

    return (
        <div className="cart-wrapper">
            <header className="top-navbar">
                <div className="logo" onClick={() => navigate("/")}>PixelStore</div>
                <div className="nav-actions">
                    <button className="logout-button" onClick={() => navigate("/product/find_all")}>Back to Store</button>
                </div>
            </header>

            <main className="cart-content">
                <h1>Your Shopping Cart</h1>

                {cartItems.length === 0 ? (
                    <div className="empty-cart">
                        <p>Your cart is empty.</p>
                        <button className="add-to-cart-btn" onClick={() => navigate("/product/find_all")}>Go Shopping</button>
                    </div>
                ) : (
                    <div className="cart-layout">
                        <div className="cart-items-list">
                            {cartItems.map((item) => (
                                <div key={item.product_id} className="cart-item-card">
                                    <img
                                        src={item.product_photos?.[0]?.image_url || "/placeholder.png"}
                                        alt={item.name}
                                        className="cart-item-img"
                                    />
                                    <div className="cart-item-info">
                                        <h3>{item.name}</h3>
                                        <p className="item-seller">Seller: {item.owner_username}</p>
                                        <p className="item-price-unit">{item.price} PLN / unit</p>
                                    </div>
                                    <div className="cart-item-controls">
                                        <button className="remove-item" onClick={() => removeItem(item.product_id)}>Remove</button>
                                    </div>
                                    <div className="cart-item-total">
                                        {(item.price * item.quantity).toFixed(2)} PLN
                                    </div>
                                </div>
                            ))}
                        </div>

                        <aside className="cart-summary">
                            <div className="summary-box">
                                <h3>Order Summary</h3>
                                <div className="summary-row">
                                    <span>Items count:</span>
                                    <span>{cartItems.reduce((a, b) => a + b.quantity, 0)}</span>
                                </div>
                                <div className="summary-row total">
                                    <span>Total Price:</span>
                                    <span>{totalPrice.toFixed(2)} PLN</span>
                                </div>
                                <button className="checkout-button" onClick={handleCheckout}>
                                    Buy Now
                                </button>
                            </div>
                        </aside>
                    </div>
                )}
            </main>
        </div>
    );
};