import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import "./index.css";
import "./App.css";

export default function App() {
  const [user, setUser] = useState(null);

  function handleLogout() {

    localStorage.removeItem("token");
    setUser(null);

  }

  if (!user) return <Login onLogin={(u) => setUser(u)} />;

  return <Dashboard user={user} onLogout={handleLogout} />;
  
}