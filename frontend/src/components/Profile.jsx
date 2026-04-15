import API from "../api/api";
import { useState } from "react";
import "./panel.css";

export default function Profile({ user, onLogout }) {
  const [name, setName] = useState(() => {
    return localStorage.getItem("profile_name") || user || "";
  });

  const [msg, setMsg] = useState(null);
  const [themeOpen, setThemeOpen] = useState(false);

  async function save() {
    try {
      await API.put("/me", { name });

      localStorage.setItem("profile_name", name);

      setMsg("Saved!");
      setTimeout(() => setMsg(null), 2000);
    } catch (e) {
      setMsg(e.response?.data?.detail || "Update failed");
      setTimeout(() => setMsg(null), 2000);
    }
  }

  // ✅ THEME TOGGLE (WORKING)
  function toggleTheme() {
    const current = localStorage.getItem("theme") || "dark";
    const next = current === "dark" ? "light" : "dark";

    localStorage.setItem("theme", next);
    document.body.className = next;

    // notify dashboard
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

      <button className="btn btn-primary" onClick={save}>
        Save Changes
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

        <div className="menu-item" onClick={onLogout}>
          🚪 Sign out
        </div>

      </div>

    </div>
  );
}