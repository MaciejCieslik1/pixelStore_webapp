import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./ProductListPage.css";
import type {ProductFromListData, ProductImage} from "../../types/product.ts";
import { findAll, type ProductFilters } from "../../api/product.ts";
import {jwtDecode} from "jwt-decode";
import type {TokenPayload} from "../../types/authentication.ts";

export const ProductListPage: React.FC = () => {
    const navigate = useNavigate();
    const [products, setProducts] = useState<ProductFromListData[]>([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [minPrice, setMinPrice] = useState<string>("");
    const [maxPrice, setMaxPrice] = useState<string>("");
    const [status, setStatus] = useState<string>("");
    const [sortBy, setSortBy] = useState("name");
    const [order, setOrder] = useState("asc");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const token = localStorage.getItem("accessToken") || "";

                const filters: ProductFilters = {
                    searchTerm: searchTerm,
                    sortBy: sortBy,
                    order: order,
                    minPrice: minPrice,
                    maxPrice: maxPrice,
                    status: status
                };

                const data = await findAll(filters, token);

                setProducts(Array.isArray(data) ? data : []);
            } catch (err) {
                console.error("Error fetching products:", err);
                setProducts([]);
            } finally {
                setLoading(false);
            }
        };

        const timeoutId = setTimeout(fetchProducts, 500);
        return () => clearTimeout(timeoutId);

    }, [searchTerm, sortBy, order, minPrice, maxPrice, status]);

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

    const selfUsername = getUsernameFromToken();

    return (
        <div className="dashboard-wrapper">
            <header className="top-navbar">
                <div className="logo" onClick={() => navigate("/")}>PixelStore</div>

                <div className="search-container">
                    <input
                        type="text"
                        placeholder="Search for products..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' &&
                            navigate(`/search?q=${searchTerm}`)}
                    />
                </div>

                <div className="nav-actions">
                    <button className="nav-btn cart-btn" onClick={() => navigate("/transaction/find_all_mine")}>
                        🛒 Cart
                    </button>

                    <button
                        className="nav-btn profile-btn"
                        onClick={() => {
                            if (selfUsername) {
                                navigate(`/user/find_by_username/${selfUsername}`);
                            } else {
                                navigate("/login");
                            }
                        }}
                    >
                        👤 My Profile
                    </button>
                </div>
            </header>

            <div className="main-content">
                <aside className="filters-sidebar">
                    <h3>Filters</h3>

                    <div className="filter-group">
                        <label>Price Range ($)</label>
                        <div className="price-inputs">
                            <input
                                type="number"
                                placeholder="Min"
                                value={minPrice}
                                onChange={(e) =>
                                    setMinPrice(e.target.value)}
                            />
                            <input
                                type="number"
                                placeholder="Max"
                                value={maxPrice}
                                onChange={(e) =>
                                    setMaxPrice(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="filter-group">
                        <label>Status</label>
                        <select value={status} onChange={(e) =>
                            setStatus(e.target.value)}>
                            <option value="">All Statuses</option>
                            <option value="available">Available</option>
                            <option value="unavailable">Unavailable</option>
                            <option value="archived">Archived</option>
                        </select>
                    </div>

                    <div className="filter-group">
                        <label>Sort by</label>
                        <select
                            value={`${sortBy}-${order}`}
                            onChange={(e) => {
                                const [field, dir] = e.target.value.split("-");
                                setSortBy(field);
                                setOrder(dir);
                            }}
                        >
                            <option value="name-asc">Name (A-Z)</option>
                            <option value="name-desc">Name (Z-A)</option>
                            <option value="price-asc">Price (Low to High)</option>
                            <option value="price-desc">Price (High to Low)</option>
                        </select>
                    </div>
                </aside>

                <section className="products-container">
                    {loading ? (
                        <div className="loader">Searching...</div>
                    ) : (
                        <div className="products-grid">
                            {products.length > 0 ? products.map((product) => {
                                const mainPhotoObj = product.product_photos?.find((img: ProductImage) =>
                                    img.is_main_photo);
                                const photoUrl = mainPhotoObj?.image_url;
                                console.log(photoUrl);

                                return (
                                    <div
                                        className="product-card"
                                        key={product.product_id}
                                        onClick={() => navigate(`/product/find_by_id/${product.product_id}`)}
                                    >
                                        <div className="product-image">
                                            {photoUrl ? (
                                                <img src={photoUrl} alt={product.name} />
                                            ) : (
                                                <div className="img-placeholder" />
                                            )}
                                        </div>
                                        <h4>{product.name}</h4>
                                        <p className="product-price">{product.price} PLN</p>
                                    </div>
                                );
                            }) : <p>No products found.</p>}
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
};