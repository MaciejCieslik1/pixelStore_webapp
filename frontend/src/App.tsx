import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import {VerifyAccountPage} from "./pages/Authentication/VerifyAccountPage.tsx";
import {RegisterPage} from "./pages/Authentication/RegisterPage.tsx";
import {LoginPage} from "./pages/Authentication/LoginPage.tsx";
import {ProductListPage} from "./pages/Product/ProductListPage.tsx";
import {ProductDetailsPage} from "./pages/Product/ProductDetailsPage.tsx"
import {CartPage} from "./pages/Order/CartPage.tsx"
import {UserProfilePage} from "./pages/User/UserProfilePage.tsx"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verify_account" element={<VerifyAccountPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/product/find_all" element={<ProductListPage />} />
        <Route path="/product/find_by_id/:product_id" element={<ProductDetailsPage />} />
        <Route path="/transaction/find_all_mine" element={<CartPage />} />
        <Route path="/user/find_by_username/:username" element={<UserProfilePage />} />
      </Routes>
    </Router>
  );
}

export default App;