import React from "react";
import "./styles/Input.css";

type InputProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: string;
};

export const Input: React.FC<InputProps> = ({ value, onChange, placeholder, type = "text" }) => {
  return (
    <input
      type={type}
      className="input"
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
    />
  );
};
