import React from "react";
import { Button } from "./Button";
import { Card } from "./Card";
import "./styles/ProductCard.css";

type ProductCardProps = {
  name: string;
  price: number;
  image: string;
  onAddToCart: () => void;
};

export const ProductCard: React.FC<ProductCardProps> = ({ name, price, image, onAddToCart }) => (
  <Card className="product-card">
    <img src={image} alt={name} className="product-img" />
    <h3 className="product-name">{name}</h3>
    <p className="product-price">{price.toFixed(2)} $</p>
    <Button className="product-btn" onClick={onAddToCart}>
      Buy
    </Button>
  </Card>
);
