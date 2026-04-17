import API from "../api/api";
import { useState } from "react";
import "./panel.css";

export default function Profile({ user, onLogout }) {
  const [name, setName] = useState(() => {
    return localStorage.getItem("profile_name") || user || "";
  });

  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [themeOpen, setThemeOpen] = useState(false);
  const [password, setPassword] = useState("");

  async function save() {

    console.log("Sending:", {
      name,
      password
    });
  
    if (!name.trim()) {
      setMsg("Name cannot be empty");
      return;
    }

    setLoading(true);

    try {
      await API.put("/me", {
        name,
        password: password || undefined
      })

      localStorage.setItem("profile_name", name);

      setMsg("Saved!");
      setTimeout(() => setMsg(null), 2000);

    } catch (e) {
      setMsg(e.response?.data?.detail || "Update failed");
      setTimeout(() => setMsg(null), 2000);

    } finally {
      setLoading(false); 
    }
  }

  function toggleTheme() {
    const current = localStorage.getItem("theme") || "dark";
    const next = current === "dark" ? "light" : "dark";

    localStorage.setItem("theme", next);
    document.body.className = next;

    window.dispatchEvent(new Event("themeChange"));
  }

  const isDark = localStorage.getItem("theme") !== "light";

  return (
    <div className="profile-container">

      {/* HEADER */}
      <div className="profile-header">
        <div className="profile-avatar">
          {name ? name[0].toUpperCase() : "U"}
        </div>

        <div>
          <p className="profile-name">{name}</p>
          <p className="profile-sub">@{user}</p>
        </div>
      </div>

      <div className="divider" />

      {/* NAME */}
      <div className="field">
        <label>Name</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div className="field">
        <label>Password</label>
        <input
          type="password"
          placeholder="New password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button
        className="btn btn-primary"
        onClick={save}
        disabled={loading}
      >
        {loading ? "Saving..." : "Save Changes"}
      </button>

      {msg && <div className="toast ok">{msg}</div>}

      <div className="divider" />

      {/* MENU */}
      <div className="profile-menu">

        <div className="menu-item">⚙ Settings</div>

        {/* APPEARANCE */}
        <div
          className="menu-item"
          onClick={() => setThemeOpen(!themeOpen)}
        >
          🎨 Appearance
        </div>

        {themeOpen && (
          <div className="theme-toggle-box">
            <div
              className={`toggle-pill ${isDark ? "dark" : "light"}`}
              onClick={toggleTheme}
            >
              <div className="toggle-circle" />

              <span className="toggle-label left">🌙</span>
              <span className="toggle-label right">☀️</span>
            </div>
          </div>
        )}

        <div className="menu-item">🔒 Security</div>

        <div
          className="menu-item"
          onClick={() => {
            localStorage.removeItem("token"); 
            onLogout();
          }}
        >
          🚪 Sign out
        </div>

      </div>

    </div>
  );
}