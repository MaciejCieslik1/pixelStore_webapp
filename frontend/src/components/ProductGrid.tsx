import React from "react";
import "./styles/ProductGrid.css";

type ProductGridProps = {
  children: React.ReactNode;
};

export const ProductGrid: React.FC<ProductGridProps> = ({ children }) => (
  <div className="product-grid">
    {children}
  </div>
);
