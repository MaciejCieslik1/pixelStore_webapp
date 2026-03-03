import React from "react";
import "./styles/Navbar.css";

type NavbarProps = {
  cartCount: number;
};

export const Navbar: React.FC<NavbarProps> = ({ cartCount }) => (
  <nav className="navbar">
    <h1 className="logo">Store</h1>

    <div className="cart-icon">
      🛒
      <span className="cart-count">{cartCount}</span>
    </div>
  </nav>
);
