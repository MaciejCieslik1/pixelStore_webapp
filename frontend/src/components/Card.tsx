import React from "react";
import "./styles/Card.css";

type CardProps = {
  children: React.ReactNode;
  className?: string;
};

export const Card: React.FC<CardProps> = ({ children, className }) => (
  <div className={`card ${className}`}>{children}</div>
);
