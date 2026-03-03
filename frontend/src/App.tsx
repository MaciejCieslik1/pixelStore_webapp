import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import {VerifyAccountPage} from "./pages/Authentication/VerifyAccountPage.tsx";
import {RegisterPage} from "./pages/Authentication/RegisterPage.tsx";
import {LoginPage} from "./pages/Authentication/LoginPage.tsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verify_account" element={<VerifyAccountPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Router>
  );
}

export default App;