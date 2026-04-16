import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import "./index.css";
import "./App.css";

export default function App() {

  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");

    if (token) {
      return localStorage.getItem("username") || "User";
    }

    return null;
  });

  function handleLogin(username) {
    localStorage.setItem("username", username);
    setUser(username);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setUser(null);
  }

  if (!user) return <Login onLogin={handleLogin} />;

  return <Dashboard user={user} onLogout={handleLogout} />;
}