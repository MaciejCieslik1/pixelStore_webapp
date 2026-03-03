import { Navbar } from "../components/Navbar";
import React from "react";

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Navbar cartCount={2} />
      <main style={{ padding: 20 }}>
        {children}
      </main>
    </>
  );
};
