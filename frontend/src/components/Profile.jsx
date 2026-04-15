import API from "../api/api";
import { useState, useEffect } from "react";
import "./panel.css";

export default function Profile({ user, onLogout }) {
  const [name, setName] = useState("");
  const [msg, setMsg] = useState(null);
  const [themeOpen, setThemeOpen] = useState(false);
  const [dark, setDark] = useState(
    localStorage.getItem("theme") !== "light"
  );

  useEffect(() => {
    const saved = localStorage.getItem("profile_name");

    setTimeout(() => {
      setName(saved || user);
    }, 0);
  }, [user]);

  // APPLY THEME
  useEffect(() => {
    document.body.classList.remove("dark", "light");
    document.body.classList.add(dark ? "dark" : "light");
  }, [dark]);

  async function save() {
    try {
      await API.put("/me", {
        name: name,
      });

      setMsg("Saved!");
      setTimeout(() => setMsg(null), 2000);

    } catch (e) {
      console.log("PROFILE ERROR:", e.response);

      setMsg(
        e.response?.data?.detail || "Update failed"
      );

      setTimeout(() => setMsg(null), 2000);
    }
  }

    function setTheme(mode) {
    const isDark = mode === "dark";

    setDark(isDark);
    localStorage.setItem("theme", mode);

    document.body.classList.remove("dark", "light");
    document.body.classList.add(mode);
    
    window.dispatchEvent(new Event("storage"));
    }

  return (
    <div className="profile-container">

      {/* TOP */}
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

      {/* EDIT NAME */}
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
          <div className="theme-box">

            <div className="theme-row">
              <span>🌙 Dark Mode</span>
              <div
                className={`switch ${dark ? "active" : ""}`}
                onClick={() => setTheme("dark")}
              >
                <div className="switch-circle" />
              </div>
            </div>

            <div className="theme-row">
              <span>☀️ Light Mode</span>
              <div
                className={`switch ${!dark ? "active" : ""}`}
                onClick={() => setTheme("light")}
              >
                <div className="switch-circle" />
              </div>
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