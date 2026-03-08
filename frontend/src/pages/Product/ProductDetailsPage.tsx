import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { findById } from "../../api/product.ts";
import type { ProductDetailsData } from "../../types/product.ts";
import { jwtDecode } from "jwt-decode";
import "./ProductDetailsPage.css";
import type {TokenPayload} from "../../types/authentication.ts";

export const ProductDetailsPage: React.FC = () => {
    const { product_id } = useParams<{ product_id: string }>();
    const navigate = useNavigate();
    const [product, setProduct] = useState<ProductDetailsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [isGalleryOpen, setIsGalleryOpen] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const token = localStorage.getItem("accessToken") || "";
                if (product_id) {
                    const data = await findById(product_id, token);
                    setProduct(data);
                }
            } catch (err) {
                console.error("Error fetching product details:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchProduct();
    }, [product_id]);

    const getUsernameFromToken = (): string | null => {
        const token = localStorage.getItem("accessToken");
        if (!token) return null;

        try {
            const decoded = jwtDecode<TokenPayload>(token);
            return decoded.username;
        } catch (err) {
            return null;
        }
    };

   const handleAddToCart = async () => {
       if (!product) {
           alert("Product data is still loading...");
           return;
       }
       const token = localStorage.getItem("accessToken");

        if (!token) {
            alert("You must be logged in to add items to the cart.");
            navigate("/login");
            return;
        }

        try {
            const transactionResponse = await fetch("http://localhost:8000/transaction/create/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    total_price: product.price,
                })
            });

            if (!transactionResponse.ok) {
                throw new Error("Failed to create transaction");
            }

            const transactionData = await transactionResponse.json();

            const orderProductResponse = await fetch("http://localhost:8000/order_product/create/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body: JSON.stringify({
                    product_id: product.product_id,
                    transaction_id: transactionData.transaction_id,
                    seller_username: product.owner_username,
                    shopping_price: Number(product.price),
                }),
            });

            if (!orderProductResponse.ok) {
                throw new Error("Order product creation error");
            }

            alert("Product was successfully added to the cart!");

        } catch (err: any) {
            console.error("Cart Error:", err);
            alert(err.message || "Error while adding product to the cart.");
        }
    };

    const selfUsername = getUsernameFromToken();

    if (loading) return <div className="loader">Loading product...</div>;
    if (!product) return <div className="error-msg">Product not found.</div>;

    const mainPhoto = product.product_photos?.find(p => p.is_main_photo)?.image_url
                      || product.product_photos?.[0]?.image_url;

    return (
        <div className="details-wrapper">
            <header className="top-navbar">
                <div className="logo" onClick={() => navigate("/")}>PixelStore</div>

                <div className="nav-actions">
                    <button className="nav-btn cart-btn" onClick={() => navigate("/transaction/find_all_mine")}>
                        🛒 Cart
                    </button>
                    <button className="nav-btn profile-btn" onClick={() => navigate(`/user/find_by_username/${selfUsername}`)}>
                        👤 My Profile
                    </button>
                </div>
            </header>

            <main className="details-content">
                <div className="product-layout">

                    <div className="product-media">
                        <div className="main-image-container" onClick={() => setIsGalleryOpen(true)}>
                            {mainPhoto ? (
                                <img src={mainPhoto} alt={product.name} className="main-img-large" />
                            ) : (
                                <div className="img-placeholder">No image available</div>
                            )}
                            <div className="zoom-overlay">Click to view gallery</div>
                        </div>
                    </div>

                    <div className="product-info-panel">
                        <div className="info-header">
                            <span className="seller-tag">Seller: {product.owner_username}</span>
                            <h1>{product.name}</h1>
                            <p className="status-badge" data-status={product.status}>{product.status}</p>
                        </div>

                        <div className="price-tag">{product.price} PLN</div>

                        <div className="description-section">
                            <h3>Description</h3>
                            <p>{product.description}</p>
                        </div>

                        <div className="specs-grid">
                            <div className="spec-item"><strong>Color:</strong> {product.color}</div>
                            <div className="spec-item"><strong>Weight:</strong> {product.weight} kg</div>
                            <div className="spec-item"><strong>Dimensions:</strong> {product.length} x {product.width} x {product.height} cm</div>
                            <div className="spec-item"><strong>Guarantee:</strong> {product.guarantee_period} months</div>
                            <div className="spec-item"><strong>In Stock:</strong> {product.amount} units</div>
                        </div>

                        <div className="action-buttons">
                            <button
                                className="add-to-cart-btn"
                                onClick={handleAddToCart}
                            >
                                Add to Cart
                            </button>

                            {selfUsername === product.owner_username && (
                                <button className="edit-product-btn" onClick={() =>
                                    navigate(`/product/update/${product.product_id}`)}>
                                    Edit Product
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </main>

            {isGalleryOpen && product.product_photos && (
                <div className="gallery-modal" onClick={() => setIsGalleryOpen(false)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <button className="close-modal" onClick={() => setIsGalleryOpen(false)}>&times;</button>
                        <img
                            src={product.product_photos[currentImageIndex].image_url}
                            alt="Gallery preview"
                        />
                        <div className="gallery-thumbs">
                            {product.product_photos.map((photo, index) => (
                                <img
                                    key={index}
                                    src={photo.image_url}
                                    className={index === currentImageIndex ? "active-thumb" : ""}
                                    onClick={() => setCurrentImageIndex(index)}
                                 alt={product.name}/>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};